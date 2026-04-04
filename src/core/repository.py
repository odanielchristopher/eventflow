from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable
from datetime import date, datetime
from pathlib import Path
from decimal import Decimal
from typing import Any, Generic, TypeVar

import pyarrow as pa
import pyarrow.dataset as ds
from deltalake import DeltaTable, write_deltalake
from pydantic import BaseModel

from src.core.storage import ensure_directory, next_sequence, sequence_path, table_path

EntityModelT = TypeVar("EntityModelT", bound=BaseModel)


class DeltaLakeRepository(Generic[EntityModelT]):
    def __init__(self, base_path: str | Path, table_name: str, model_cls: type[EntityModelT]) -> None:
        self._base_path = Path(base_path)
        self._table_name = table_name
        self._model_cls = model_cls
        self._table_dir = table_path(self._base_path, table_name)
        self._seq_file = sequence_path(self._base_path, table_name)
        ensure_directory(self._table_dir)

    def create(self, data: EntityModelT | dict[str, Any]) -> EntityModelT:
        payload = self._normalize_payload(data)
        if payload.get("id") is None:
            payload["id"] = next_sequence(self._seq_file)
        else:
            self._sync_sequence(int(payload["id"]))

        self._append_rows([payload])
        return self._to_model(payload)

    insert = create

    def find_unique(self, record_id: int) -> EntityModelT | None:
        records = self._read_rows(filters={"id": record_id}, limit=1)
        if not records:
            return None
        return self._to_model(records[0])

    get = find_unique

    def find_many(
        self,
        *,
        where: dict[str, Any] | None = None,
        select: tuple[str, ...] | list[str] | None = None,
        order_by: list[tuple[str, str]] | None = None,
        group_by: tuple[str, ...] | list[str] | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> list[Any]:
        rows = self._read_rows(
            filters=where or {},
            selected_fields=tuple(select or ()),
            order_by=order_by or [],
            group_by=tuple(group_by or ()),
            limit=page_size,
            offset=max(page - 1, 0) * page_size,
        )

        if select:
            return rows

        if group_by:
            return rows

        return [self._to_model(row) for row in rows]

    list = find_many

    def update(self, record_id: int, data: EntityModelT | dict[str, Any]) -> EntityModelT | None:
        if self.find_unique(record_id) is None:
            return None

        payload = self._normalize_payload(data)
        payload.pop("id", None)

        table = self._load_table()
        if table is None:
            return None

        table.update(
            predicate=self._predicate_for_id(record_id),
            updates={field: self._to_sql_literal(value) for field, value in payload.items()},
        )
        return self.find_unique(record_id)

    def upsert(self, record_id: int, data: EntityModelT | dict[str, Any]) -> EntityModelT:
        existing = self.find_unique(record_id)
        if existing is None:
            payload = self._normalize_payload(data)
            payload["id"] = record_id
            return self.create(payload)

        updated = self.update(record_id, data)
        return updated or existing

    def delete(self, record_id: int) -> bool:
        if self.find_unique(record_id) is None:
            return False

        table = self._load_table()
        if table is None:
            return False

        table.delete(predicate=self._predicate_for_id(record_id))
        return True

    def count(self, where: dict[str, Any] | None = None) -> int:
        table = self._load_table()
        if table is None:
            return 0

        filter_expr = self._build_filter_expression(where or {})
        dataset = table.to_pyarrow_dataset()
        return int(dataset.count_rows(filter=filter_expr))

    def vacuum(self) -> list[str]:
        table = self._load_table()
        if table is None:
            return []

        try:
            return table.vacuum(retention_hours=0, enforce_retention_duration=False)
        except TypeError:
            return table.vacuum()

    def export_batches(
        self,
        *,
        where: dict[str, Any] | None = None,
        select: tuple[str, ...] | list[str] | None = None,
        batch_size: int = 1000,
    ):
        table = self._load_table()
        if table is None:
            yield from ()
            return

        columns = list(select) if select is not None else None

        scanner = self._scanner(
            table,
            filters=where or {},
            columns=columns,
            batch_size=batch_size
        )

        for batch in scanner.to_batches():
            yield batch.to_pylist()

    def _read_rows(
        self,
        *,
        filters: dict[str, Any],
        selected_fields: tuple[str, ...] = (),
        order_by: list[tuple[str, str]] | None = None,
        group_by: tuple[str, ...] = (),
        limit: int | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        table = self._load_table()
        if table is None:
            return []

        use_full_scan = bool(order_by or group_by)
        rows = self._scan_rows(
            table,
            filters=filters,
            selected_fields=selected_fields,
            limit=None if use_full_scan else limit,
            offset=0 if use_full_scan else offset,
        )

        if order_by:
            for field, direction in reversed(order_by):
                reverse = direction.lower() == "desc"
                rows.sort(key=lambda item: item.get(field), reverse=reverse)

        if group_by:
            grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
            for row in rows:
                key = tuple(row.get(field) for field in group_by)
                grouped[key].append(row)

            grouped_rows: list[dict[str, Any]] = []
            for key, items in grouped.items():
                grouped_rows.append(
                    {
                        "group": {field: key[index] for index, field in enumerate(group_by)},
                        "items": items,
                        "count": len(items),
                    }
                )
            rows = grouped_rows

        if use_full_scan and (offset or limit is not None):
            rows = rows[offset : offset + limit if limit is not None else None]

        return rows

    def _scan_rows(
        self,
        table: DeltaTable,
        *,
        filters: dict[str, Any],
        selected_fields: tuple[str, ...],
        limit: int | None,
        offset: int,
    ) -> list[dict[str, Any]]:
        columns = list(selected_fields) or None
        scanner = self._scanner(
            table,
            filters=filters,
            columns=columns,
            batch_size=max(limit or 1000, 1),
        )
        rows: list[dict[str, Any]] = []
        skipped = 0

        for batch in scanner.to_batches():
            for row in batch.to_pylist():
                if skipped < offset:
                    skipped += 1
                    continue
                rows.append(row)
                if limit is not None and len(rows) >= limit:
                    return rows
        return rows

    def _scanner(
        self,
        table: DeltaTable,
        *,
        filters: dict[str, Any],
        columns: list[str] | None,
        batch_size: int,
    ):
        dataset = table.to_pyarrow_dataset()
        filter_expr = self._build_filter_expression(filters)
        return dataset.scanner(columns=columns, filter=filter_expr, batch_size=batch_size)

    def _build_filter_expression(self, filters: dict[str, Any]):
        expression = None
        for field_name, value in filters.items():
            condition = ds.field(field_name) == value
            expression = condition if expression is None else expression & condition
        return expression

    def _append_rows(self, rows: list[dict[str, Any]]) -> None:
        table = pa.Table.from_pylist(rows)
        write_deltalake(self._table_dir.as_posix(), table, mode="append")

    def _load_table(self) -> DeltaTable | None:
        if not self._table_dir.exists():
            return None
        try:
            return DeltaTable(self._table_dir.as_posix())
        except Exception:
            return None

    def _to_model(self, payload: dict[str, Any]) -> EntityModelT:
        return self._model_cls.model_validate(payload)

    def _normalize_payload(self, data: EntityModelT | dict[str, Any]) -> dict[str, Any]:
        if isinstance(data, BaseModel):
            return data.model_dump(exclude_none=True)
        return dict(data)

    def _sync_sequence(self, record_id: int) -> None:
        current = 0
        if self._seq_file.exists():
            try:
                current = int(self._seq_file.read_text(encoding="utf-8").strip() or "0")
            except ValueError:
                current = 0
        if record_id > current:
            self._seq_file.write_text(f"{record_id}\n", encoding="utf-8")

    def _predicate_for_id(self, record_id: int) -> str:
        return f"id == {record_id}"

    def _to_sql_literal(self, value: Any) -> str:
        if isinstance(value, str):
            escaped = value.replace("'", "''")
            return f"'{escaped}'"

        if isinstance(value, bool):
            return "true" if value else "false"

        if isinstance(value, datetime):
            return f"TIMESTAMP '{value.isoformat(sep=' ')}'"

        if isinstance(value, date):
            return f"DATE '{value.isoformat()}'"

        if isinstance(value, Decimal):
            return format(value, "f")

        if isinstance(value, (int, float)):
            return str(value)

        raise TypeError(f"Unsupported value for SQL update literal: {value!r}")
