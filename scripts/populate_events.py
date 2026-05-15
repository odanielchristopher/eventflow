from __future__ import annotations

import argparse
import asyncio
import random
import sys
from decimal import Decimal
from pathlib import Path

from faker import Faker
from sqlalchemy import select


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.infra.db.session import session_factory
from src.models.event import EventCreate, EventEntity

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

EVENT_LOCATIONS = [
    "Centro de Eventos - Fortaleza/CE",
    "Expo Center - Recife/PE",
    "Pavilhao Tech - Salvador/BA",
    "Arena Inovacao - Sao Paulo/SP",
    "Convention Hall - Natal/RN",
    "Campus Summit - Joao Pessoa/PB",
    "Centro Empresarial - Belo Horizonte/MG",
    "Espaco Criativo - Curitiba/PR",
    "Hub de Negocios - Brasilia/DF",
    "Parque de Exposicoes - Porto Alegre/RS",
]


def build_event(fake: Faker, event_number: int, used_date_locations: set[tuple[object, str]]) -> EventCreate:
    while True:
        event_date = fake.date_between(start_date="-180d", end_date="+365d")
        location = random.choice(EVENT_LOCATIONS)
        date_location = (event_date, location)
        if date_location not in used_date_locations:
            used_date_locations.add(date_location)
            break

    capacity = random.randint(40, 800)
    price = Decimal(f"{random.uniform(0, 850):.2f}")

    return EventCreate(
        title=f"{random.choice(EVENT_FORMATS).format(topic=random.choice(EVENT_TOPICS))} {event_number}",
        description=f"{fake.text(max_nb_chars=180)} Ref. seed {event_number}",
        date=event_date,
        location=location,
        capacity=capacity,
        sub_price=price,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Populate the event minibanco with fake data.")
    parser.add_argument("--count", type=int, default=1000, help="Number of events to create (default: 1000).")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible data (default: 42).")
    return parser.parse_args()


async def run_seed(count: int, seed: int) -> None:
    random.seed(seed)
    fake = Faker("pt_BR")
    fake.seed_instance(seed)

    async with session_factory() as session:
        existing_result = await session.execute(select(EventEntity))
        existing_events = list(existing_result.scalars().all())

        used_date_locations = {(event.date, event.location) for event in existing_events}
        start_index = len(existing_events) + 1

        rows = [
            EventEntity.model_validate(
                build_event(fake, start_index + index, used_date_locations).model_dump()
            )
            for index in range(count)
        ]

        session.add_all(rows)
        await session.commit()

    print(f"Created {count} events")


def main() -> None:
    args = parse_args()
    if args.count < 1:
        raise SystemExit("Use at least 1 registros.")
    asyncio.run(run_seed(args.count, args.seed))


if __name__ == "__main__":
    main()
