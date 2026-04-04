from __future__ import annotations

import argparse
import random
import sys
from decimal import Decimal
from pathlib import Path

from faker import Faker
import pyarrow as pa
from deltalake import write_deltalake


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.models import CreateEventDto
from src.core.storage import sequence_value, write_sequence

EVENT_FORMATS = [
    "Congresso de {topic}",
    "Encontro de {topic}",
    "Feira de {topic}",
    "Summit de {topic}",
    "Jornada de {topic}",
    "Workshop de {topic}",
    "Festival de {topic}",
]

EVENT_TOPICS = [
    "Tecnologia",
    "Inovação",
    "Empreendedorismo",
    "Saúde",
    "Educação",
    "Marketing",
    "Dados",
    "Sustentabilidade",
    "Finanças",
    "Design",
]


def build_event(fake: Faker, event_id: int) -> dict[str, object]:
    event_date = fake.date_between(start_date="-180d", end_date="+365d")
    capacity = random.randint(40, 800)
    price = Decimal(f"{random.uniform(0, 850):.2f}")

    dto = CreateEventDto(
        title=random.choice(EVENT_FORMATS).format(topic=random.choice(EVENT_TOPICS)),
        description=fake.text(max_nb_chars=220),
        date=event_date,
        location=f"{fake.city()} - {fake.state_abbr()}",
        capacity=capacity,
        sub_price=price,
    )
    return {"id": event_id, **dto.model_dump()}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Populate the event minibanco with fake data.")
    parser.add_argument("--count", type=int, default=1000, help="Number of events to create (default: 1000).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible data (default: 42).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.count < 1000:
        raise SystemExit("Use at least 1000 registros.")

    random.seed(args.seed)
    fake = Faker("pt_BR")
    fake.seed_instance(args.seed)

    table_dir = ROOT / "src" / "data" / "events"
    seq_file = ROOT / "src" / "data" / "events.seq"

    start_id = sequence_value(seq_file)
    rows = [build_event(fake, start_id + index + 1) for index in range(args.count)]

    table = pa.Table.from_pylist(rows)
    write_deltalake(table_dir.as_posix(), table, mode="append")
    write_sequence(seq_file, start_id + args.count)

    print(f"Created {args.count} events")


if __name__ == "__main__":
    main()
