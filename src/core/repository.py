from __future__ import annotations

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
        # Guarda a configuração da tabela e prepara a pasta física do Delta Lake.
        self._base_path = Path(base_path)
        self._table_name = table_name
        self._model_cls = model_cls
        self._table_dir = table_path(self._base_path, table_name)
        self._seq_file = sequence_path(self._base_path, table_name)
        ensure_directory(self._table_dir)

    def create(self, data: EntityModelT | dict[str, Any]) -> EntityModelT:
        # Normaliza o payload, gera o id e grava a linha como um novo commit.
        payload = self._normalize_payload(data)
        if payload.get("id") is None:
            payload["id"] = next_sequence(self._seq_file)
        else:
            self._sync_sequence(int(payload["id"]))

        self._append_rows([payload])
        return self._to_model(payload)

    insert = create

    def find_unique(self, record_id: int) -> EntityModelT | None:
        # Busca um único registro pelo id.
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
        limit: int = 20,
        offset: int = 0,
    ) -> list[Any]:
        # Mantém a interface pública com paginação simples, mas lê em lotes pequenos.
        rows = self._read_rows(
            filters=where or {},
            selected_fields=tuple(select or ()),
            limit=limit,
            offset=max(offset, 0),
        )

        if select:
            return rows

        return [self._to_model(row) for row in rows]

    list = find_many

    def update(self, record_id: int, data: EntityModelT | dict[str, Any]) -> EntityModelT | None:
        # Atualiza um registro existente e devolve o estado já recarregado.
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
        # Se o id já existir, faz update; caso contrário, cria um novo registro.
        existing = self.find_unique(record_id)
        if existing is None:
            payload = self._normalize_payload(data)
            payload["id"] = record_id
            return self.create(payload)

        updated = self.update(record_id, data)
        return updated or existing

    def delete(self, record_id: int) -> bool:
        # Remove um registro somente quando ele já existe na tabela.
        if self.find_unique(record_id) is None:
            return False

        table = self._load_table()
        if table is None:
            return False

        table.delete(predicate=self._predicate_for_id(record_id))
        return True

    def count(self, where: dict[str, Any] | None = None) -> int:
        # Conta registros direto no dataset, sem montar a lista inteira em memória.
        table = self._load_table()
        if table is None:
            return 0

        filter_expr = self._build_filter_expression(where or {})
        dataset = table.to_pyarrow_dataset()
        return int(dataset.count_rows(filter=filter_expr))

    def vacuum(self) -> list[str]:
        # Limpa arquivos antigos do Delta Lake, com fallback para compatibilidade.
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
        # Exporta em lotes para permitir streaming sem carregar tudo na RAM.
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
        limit: int | None = None,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        # Faz a leitura base do dataset usando lotes do próprio scanner.
        # Assim, o código lê só a janela pedida sem montar a tabela inteira em RAM.
        table = self._load_table()
        if table is None:
            return []

        columns = list(selected_fields) or None
        scanner = self._scanner(
            table,
            filters=filters,
            columns=columns,
            batch_size=max(limit or 1, 1),
        )

        rows: list[dict[str, Any]] = []
        skipped = 0
        page_size = max(limit or 1, 1)

        for batch in scanner.to_batches():
            batch_rows = batch.to_pylist()

            if skipped + len(batch_rows) <= offset:
                skipped += len(batch_rows)
                continue

            start = max(offset - skipped, 0)
            rows.extend(batch_rows[start:])
            skipped += len(batch_rows)

            if len(rows) >= page_size:
                return rows[:page_size]

        return rows[:page_size]

    def _scanner(
        self,
        table: DeltaTable,
        *,
        filters: dict[str, Any],
        columns: list[str] | None,
        batch_size: int,
    ):
        # Cria o scanner do dataset com filtros e tamanho de lote definidos.
        dataset = table.to_pyarrow_dataset()
        filter_expr = self._build_filter_expression(filters)
        return dataset.scanner(columns=columns, filter=filter_expr, batch_size=batch_size)

    def _build_filter_expression(self, filters: dict[str, Any]):
        # Combina os filtros com AND para o dataset poder aplicar pushdown.
        expression = None
        for field_name, value in filters.items():
            condition = self._build_field_condition(field_name, value)
            expression = condition if expression is None else expression & condition
        return expression

    def _build_field_condition(self, field_name: str, value: Any):
        # Converte um filtro simples ou composto para uma expressão do PyArrow.
        field = ds.field(field_name)

        if isinstance(value, dict):
            condition = None
            for operator, operand in value.items():
                if operator == "eq":
                    expr = field == operand
                elif operator == "ne":
                    expr = field != operand
                elif operator == "gt":
                    expr = field > operand
                elif operator == "gte":
                    expr = field >= operand
                elif operator == "lt":
                    expr = field < operand
                elif operator == "lte":
                    expr = field <= operand
                else:
                    raise ValueError(f"Unsupported filter operator: {operator}")

                condition = expr if condition is None else condition & expr
            return condition

        return field == value

    def _append_rows(self, rows: list[dict[str, Any]]) -> None:
        # Cada append vira um novo commit do Delta Lake.
        table = pa.Table.from_pylist(rows)
        write_deltalake(self._table_dir.as_posix(), table, mode="append")

    def _load_table(self) -> DeltaTable | None:
        # Abre a tabela Delta no diretório físico, se ela já existir.
        if not self._table_dir.exists():
            return None
        try:
            return DeltaTable(self._table_dir.as_posix())
        except Exception:
            return None

    def _to_model(self, payload: dict[str, Any]) -> EntityModelT:
        # Valida e converte o payload bruto para o model do domínio.
        return self._model_cls.model_validate(payload)

    def _normalize_payload(self, data: EntityModelT | dict[str, Any]) -> dict[str, Any]:
        # Aceita model Pydantic ou dict puro e devolve um payload serializável.
        if isinstance(data, BaseModel):
            return data.model_dump(exclude_none=True)
        return dict(data)

    def _sync_sequence(self, record_id: int) -> None:
        # Mantém o arquivo de sequência sempre alinhado com o maior id gravado.
        current = 0
        if self._seq_file.exists():
            try:
                current = int(self._seq_file.read_text(encoding="utf-8").strip() or "0")
            except ValueError:
                current = 0
        if record_id > current:
            self._seq_file.write_text(f"{record_id}\n", encoding="utf-8")

    def _predicate_for_id(self, record_id: int) -> str:
        # Monta a condição SQL usada para localizar o registro pelo id.
        return f"id == {record_id}"

    def _to_sql_literal(self, value: Any) -> str:
        # Converte valores Python para literais SQL aceitos pelo update do Delta Lake.
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
