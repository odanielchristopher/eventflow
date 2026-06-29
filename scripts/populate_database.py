from __future__ import annotations

import argparse
import asyncio
import random
import sys
from datetime import datetime, time, timedelta
from decimal import Decimal
from pathlib import Path

from faker import Faker

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.infra.db.mongo import close_mongo, init_mongo
from src.models.checkin import CheckIn
from src.models.document import Document
from src.models.event import EventEntity
from src.models.speaker import Speaker
from src.models.subscription import Subscription

EVENT_FORMATS = [
    "Congresso Brasileiro de {topic}",
    "Encontro Regional de {topic}",
    "Feira Nacional de {topic}",
    "Summit de {topic}",
    "Jornada de {topic}",
    "Workshop Avancado de {topic}",
    "Forum de {topic}",
]

EVENT_TOPICS = [
    "Tecnologia",
    "Inovacao",
    "Empreendedorismo",
    "Saude Digital",
    "Educacao",
    "Marketing",
    "Dados",
    "Sustentabilidade",
    "Financas",
    "Design",
    "Gestao Publica",
    "Cultura",
]

EVENT_LOCATIONS = [
    "Centro de Eventos do Ceara - Fortaleza/CE",
    "Expo Center Norte - Sao Paulo/SP",
    "Riocentro - Rio de Janeiro/RJ",
    "Centro de Convencoes de Pernambuco - Olinda/PE",
    "Centro de Convencoes Salvador - Salvador/BA",
    "Expominas - Belo Horizonte/MG",
    "Centro de Eventos FIERGS - Porto Alegre/RS",
    "Viasoft Experience - Curitiba/PR",
    "Centro de Convencoes Ulysses Guimaraes - Brasilia/DF",
    "Centro de Convencoes de Natal - Natal/RN",
    "Centro de Convencoes de Joao Pessoa - Joao Pessoa/PB",
    "Hangar Convencoes e Feiras da Amazonia - Belem/PA",
]

SPECIALTIES = [
    "Engenharia de Software",
    "Experiencia do Usuario",
    "Ciencia de Dados",
    "Marketing Digital",
    "Gestao de Projetos",
    "Inovacao Corporativa",
    "Ciberseguranca",
    "Sustentabilidade",
    "Financas para Negocios",
    "Saude Publica",
    "Educacao e Tecnologia",
    "Produto Digital",
]

DOCUMENT_KINDS = [
    ("programacao", "application/pdf", ".pdf"),
    ("mapa-do-evento", "application/pdf", ".pdf"),
    ("regulamento", "application/pdf", ".pdf"),
    ("banner", "image/jpeg", ".jpg"),
    ("material-de-apoio", "application/pdf", ".pdf"),
    ("certificado-modelo", "application/pdf", ".pdf"),
]

ACCESS_POINTS = [
    "Entrada principal",
    "Credenciamento A",
    "Credenciamento B",
    "Portao lateral",
    "Acesso VIP",
    "Auditorio central",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Popula o MongoDB configurado no .env com dados realistas."
    )
    parser.add_argument(
        "--count-per-entity",
        "--count",
        type=int,
        default=100,
        help="Quantidade de registros por entidade principal (minimo e padrao: 100).",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed usada para tornar a geracao reproduzivel (padrao: 42).",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Remove os dados das colecoes antes de popular novamente.",
    )
    return parser.parse_args()


def money(value: float) -> Decimal:
    return Decimal(f"{value:.2f}")


def build_event(
    number: int,
    fake: Faker,
    used_titles: set[str],
    used_descriptions: set[str],
    used_date_locations: set[tuple[object, str]],
) -> EventEntity:
    while True:
        topic = random.choice(EVENT_TOPICS)
        title = f"{random.choice(EVENT_FORMATS).format(topic=topic)} {number:04d}"
        if title not in used_titles:
            used_titles.add(title)
            break

    while True:
        event_date = fake.date_between(start_date="+15d", end_date="+720d")
        location = random.choice(EVENT_LOCATIONS)
        date_location = (event_date, location)
        if date_location not in used_date_locations:
            used_date_locations.add(date_location)
            break

    while True:
        description = (
            f"{title} reunira profissionais e estudantes em {location.split(' - ')[0]} "
            f"para discutir {topic.lower()}, tendencias de mercado e experiencias praticas. "
            f"Codigo de carga {number:04d}."
        )
        if description not in used_descriptions:
            used_descriptions.add(description)
            break

    return EventEntity(
        title=title,
        description=description,
        banner_img_url=f"https://cdn.eventflow.local/banners/evento-{number:04d}.jpg",
        date=event_date,
        location=location,
        capacity=random.randint(80, 1200),
        sub_price=money(random.uniform(0, 950)),
    )


def build_speaker(number: int, fake: Faker) -> Speaker:
    specialty = random.choice(SPECIALTIES)
    name = fake.name()
    return Speaker(
        name=name,
        specialty=specialty,
        bio=(
            f"{name} atua em {specialty.lower()} e participa de projetos, aulas e "
            f"consultorias para organizacoes brasileiras. Perfil de carga {number:04d}."
        ),
    )


def build_document(number: int, event: EventEntity) -> Document:
    kind, content_type, extension = random.choice(DOCUMENT_KINDS)
    return Document(
        original_filename=f"{kind}-evento-{str(event.id)}-{number:04d}{extension}",
        content_type=content_type,
        extension=extension,
        size_bytes=random.randint(64_000, 8_000_000),
        event_id=str(event.id),
    )


def build_check_in(event: EventEntity) -> CheckIn:
    return CheckIn(
        timestamp=datetime.combine(
            event.date,
            time(hour=random.randint(7, 21), minute=random.randint(0, 59)),
        ),
        access_point=random.choice(ACCESS_POINTS),
    )


def build_subscription(number: int, fake: Faker, event: EventEntity) -> Subscription:
    registered_at = event.date - timedelta(days=random.randint(1, 120))
    email_user = fake.user_name().replace(".", "-")
    has_check_in = random.random() < 0.75
    return Subscription(
        name=fake.name(),
        email=f"participante.{number:04d}.{email_user}@example.com",
        price=event.sub_price,
        registered_at=registered_at,
        event_id=str(event.id),
        check_in=build_check_in(event) if has_check_in else None,
    )


async def reset_collections() -> None:
    await Subscription.delete_all()
    await Document.delete_all()
    await Speaker.delete_all()
    await EventEntity.delete_all()


async def next_sequence_start(model, field: str, fallback: int = 0) -> int:
    total = await model.count()
    if total == 0:
        return fallback + 1
    return total + fallback + 1


async def run_seed(count_per_entity: int, seed: int, reset: bool) -> None:
    if count_per_entity < 100:
        raise SystemExit("Use --count-per-entity com pelo menos 100 registros.")

    random.seed(seed)
    fake = Faker("pt_BR")
    fake.seed_instance(seed)

    await init_mongo()
    try:
        if reset:
            await reset_collections()

        existing_events = await EventEntity.find_all().to_list()
        used_titles = {event.title for event in existing_events}
        used_descriptions = {event.description for event in existing_events}
        used_date_locations = {(event.date, event.location) for event in existing_events}
        event_start = await next_sequence_start(EventEntity, "title")
        speaker_start = await next_sequence_start(Speaker, "name")
        subscription_start = await next_sequence_start(Subscription, "email")

        events = [
            build_event(
                event_start + index,
                fake,
                used_titles,
                used_descriptions,
                used_date_locations,
            )
            for index in range(count_per_entity)
        ]
        await EventEntity.insert_many(events)

        speakers = [
            build_speaker(speaker_start + index, fake)
            for index in range(count_per_entity)
        ]
        await Speaker.insert_many(speakers)

        documents = [
            build_document(index + 1, events[index % len(events)])
            for index in range(count_per_entity)
        ]
        await Document.insert_many(documents)

        subscriptions = [
            build_subscription(
                subscription_start + index,
                fake,
                events[index % len(events)],
            )
            for index in range(count_per_entity)
        ]
        await Subscription.insert_many(subscriptions)

        check_in_count = sum(1 for subscription in subscriptions if subscription.check_in)

        print("Populate concluido com sucesso:")
        print(f"- {len(events)} eventos")
        print(f"- {len(speakers)} palestrantes")
        print(f"- {len(documents)} documentos")
        print(f"- {len(subscriptions)} inscricoes")
        print(f"- {check_in_count} check-ins embutidos em inscricoes")
    finally:
        await close_mongo()


def main() -> None:
    args = parse_args()
    asyncio.run(run_seed(args.count_per_entity, args.seed, args.reset))


if __name__ == "__main__":
    main()
