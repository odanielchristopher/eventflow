from __future__ import annotations

import argparse
import asyncio
import random
import sys
from datetime import datetime, time, timedelta
from decimal import Decimal
from pathlib import Path

from faker import Faker
from sqlalchemy import func, select

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.infra.db.models import (
    Activity,
    ActivitySpeaker,
    CheckIn,
    Document,
    Event,
    Speaker,
    Subscription,
)
from src.infra.db.session import session_factory

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

ACTIVITY_TYPES = [
    "Palestra",
    "Mesa-redonda",
    "Oficina",
    "Painel",
    "Mentoria coletiva",
    "Estudo de caso",
    "Sessao tecnica",
    "Laboratorio pratico",
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
        description="Popula o banco configurado no .env com dados realistas para todas as entidades."
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
    return parser.parse_args()


def money(value: float) -> Decimal:
    return Decimal(f"{value:.2f}")


def build_event(
    fake: Faker,
    number: int,
    used_titles: set[str],
    used_descriptions: set[str],
    used_date_locations: set[tuple[object, str]],
) -> Event:
    while True:
        topic = random.choice(EVENT_TOPICS)
        title = f"{random.choice(EVENT_FORMATS).format(topic=topic)} {number:04d}"
        if title not in used_titles:
            used_titles.add(title)
            break

    while True:
        event_date = fake.date_between(start_date="-180d", end_date="+720d")
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

    return Event(
        title=title,
        description=description,
        banner_img_url=f"https://cdn.eventflow.local/banners/evento-{number:04d}.jpg",
        date=event_date,
        location=location,
        capacity=random.randint(80, 1200),
        sub_price=money(random.uniform(0, 950)),
    )


def build_speaker(fake: Faker, number: int) -> Speaker:
    specialty = random.choice(SPECIALTIES)
    return Speaker(
        name=fake.name(),
        specialty=specialty,
        bio=(
            f"{fake.name()} atua em {specialty.lower()} e participa de projetos, aulas e "
            f"consultorias para organizacoes brasileiras. Perfil de carga {number:04d}."
        ),
    )


def build_activity(event: Event, number: int) -> Activity:
    topic = random.choice(EVENT_TOPICS)
    scheduled_hour = random.randint(8, 20)
    scheduled_minute = random.choice([0, 15, 30, 45])
    return Activity(
        title=f"{random.choice(ACTIVITY_TYPES)}: {topic} na pratica {number:04d}",
        scheduled_at=time(hour=scheduled_hour, minute=scheduled_minute),
        event_id=event.id,
    )


def build_document(event: Event, number: int) -> Document:
    kind, content_type, extension = random.choice(DOCUMENT_KINDS)
    return Document(
        original_filename=f"{kind}-evento-{event.id}-{number:04d}{extension}",
        content_type=content_type,
        extension=extension,
        size_bytes=random.randint(64_000, 8_000_000),
        event_id=event.id,
    )


def build_subscription(fake: Faker, event: Event, number: int) -> Subscription:
    registered_at = event.date - timedelta(days=random.randint(1, 120))
    email_user = fake.user_name().replace(".", "-")
    return Subscription(
        name=fake.name(),
        email=f"participante.{number:04d}.{email_user}@example.com",
        price=event.sub_price,
        registered_at=registered_at,
        event_id=event.id,
    )


def build_check_in(subscription: Subscription, event: Event) -> CheckIn:
    return CheckIn(
        timestamp=datetime.combine(
            event.date,
            time(hour=random.randint(7, 21), minute=random.randint(0, 59)),
        ),
        access_point=random.choice(ACCESS_POINTS),
        subscription_id=subscription.id,
    )


async def run_seed(count_per_entity: int, seed: int) -> None:
    if count_per_entity < 100:
        raise SystemExit("Use --count-per-entity com pelo menos 100 registros.")

    random.seed(seed)
    fake = Faker("pt_BR")
    fake.seed_instance(seed)

    async with session_factory() as session:
        existing_events = (await session.execute(select(Event))).scalars().all()
        used_titles = {event.title for event in existing_events}
        used_descriptions = {event.description for event in existing_events}
        used_date_locations = {(event.date, event.location) for event in existing_events}

        max_event_id = (await session.execute(select(func.max(Event.id)))).scalar_one() or 0
        max_speaker_id = (await session.execute(select(func.max(Speaker.id)))).scalar_one() or 0
        max_subscription_id = (await session.execute(select(func.max(Subscription.id)))).scalar_one() or 0

        events = [
            build_event(
                fake,
                max_event_id + index + 1,
                used_titles,
                used_descriptions,
                used_date_locations,
            )
            for index in range(count_per_entity)
        ]
        speakers = [
            build_speaker(fake, max_speaker_id + index + 1)
            for index in range(count_per_entity)
        ]

        session.add_all(events)
        session.add_all(speakers)
        await session.flush()

        activities = [
            build_activity(events[index % len(events)], index + 1)
            for index in range(count_per_entity)
        ]
        documents = [
            build_document(events[index % len(events)], index + 1)
            for index in range(count_per_entity)
        ]
        subscriptions = [
            build_subscription(
                fake,
                events[index % len(events)],
                max_subscription_id + index + 1,
            )
            for index in range(count_per_entity)
        ]

        session.add_all(activities)
        session.add_all(documents)
        session.add_all(subscriptions)
        await session.flush()

        activity_speakers = []
        for index, activity in enumerate(activities):
            selected_speakers = random.sample(
                speakers,
                k=random.randint(1, min(3, len(speakers))),
            )
            activity_speakers.extend(
                ActivitySpeaker(activity_id=activity.id, speaker_id=speaker.id)
                for speaker in selected_speakers
            )

        check_ins = [
            build_check_in(subscription, events[index % len(events)])
            for index, subscription in enumerate(subscriptions)
        ]

        session.add_all(activity_speakers)
        session.add_all(check_ins)
        await session.commit()

    print("Populate concluido com sucesso:")
    print(f"- {len(events)} eventos")
    print(f"- {len(speakers)} palestrantes")
    print(f"- {len(activities)} atividades")
    print(f"- {len(activity_speakers)} vinculos entre atividades e palestrantes")
    print(f"- {len(documents)} documentos")
    print(f"- {len(subscriptions)} inscricoes")
    print(f"- {len(check_ins)} check-ins")


def main() -> None:
    args = parse_args()
    asyncio.run(run_seed(args.count_per_entity, args.seed))


if __name__ == "__main__":
    main()
