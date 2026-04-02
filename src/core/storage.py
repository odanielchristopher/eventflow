from __future__ import annotations

from pathlib import Path


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def sequence_value(path: Path) -> int:
    if not path.exists():
        return 0
    raw = path.read_text(encoding="utf-8").strip()
    return int(raw or "0")


def write_sequence(path: Path, value: int) -> None:
    ensure_directory(path.parent)
    path.write_text(f"{value}\n", encoding="utf-8")


def next_sequence(path: Path) -> int:
    current = sequence_value(path)
    current += 1
    write_sequence(path, current)
    return current


def table_path(base_path: Path, table_name: str) -> Path:
    return base_path / table_name


def sequence_path(base_path: Path, table_name: str) -> Path:
    return base_path / f"{table_name}.seq"
