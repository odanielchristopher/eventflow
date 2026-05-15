# EventFlow API

A EventFlow API é um projeto FastAPI para gerenciamento de eventos, inscrições, atividades, palestrantes, check-ins e documentos.

O projeto usa `SQLModel`, `Alembic` e persistência relacional assíncrona com suporte a SQLite e PostgreSQL.

## Stack Atual De Dependências

- `FastAPI`
- `SQLModel`
- `SQLAlchemy` assíncrono
- `Alembic`
- `Pydantic`
- `fastapi-pagination`
- `asyncpg` para PostgreSQL
- `aiosqlite` para SQLite
- `python-dotenv` para configuração via `.env`
- `python-multipart` para upload de arquivos

## Arquitetura Definida

A arquitetura escolhida para a próxima etapa do projeto é esta:

```text
src/
  core/
  infra/
    db/
    repositories/
  models/
    event/
      entity.py
      schemas.py
    document/
      entity.py
      schemas.py
    speaker/
      entity.py
      schemas.py
    activity/
      entity.py
      schemas.py
    subscription/
      entity.py
      schemas.py
    checkin/
      entity.py
      schemas.py
  dependencies/
  routes/
  usecases/
```

## Responsabilidades Das Camadas

- `core/` concentra configuração compartilhada, constantes, exceptions e utilitários centrais.
- `infra/db/` concentra engine assíncrona, sessions, configuração do banco e integração com SQLModel/Alembic.
- `infra/repositories/` implementa os repositórios concretos que acessam o banco.
- `models/` organiza o domínio por entidade.
- `entity.py` define os modelos de persistência com `SQLModel`.
- `schemas.py` define os contratos da API, como create, update, read e filtros.
- `dependencies/` usa o mecanismo nativo de dependências do FastAPI para montar sessão, repositórios e use cases.
- `routes/` expõe os endpoints HTTP.
- `usecases/` concentra as regras de negócio e não deve conhecer detalhes do banco usado.

## Injeção De Dependências

O projeto vai utilizar a forma nativa do FastAPI para composição de dependências com `Depends(...)`.

Com isso:

- as `routes` recebem as dependências prontas;
- as `dependencies` montam `session -> repository -> usecase`;
- os `usecases` dependem de abstrações e não do banco diretamente;
- os `repositories` encapsulam o acesso ao `SQLModel` e ao `AsyncSession`.

## Domínio Do Projeto

As entidades principais do domínio são:

- `Event`
- `Document`
- `Speaker`
- `Activity`
- `Subscription`
- `CheckIn`

O relacionamento com documentos será modelado para atender ao requisito do trabalho. Um evento poderá possuir um ou mais documentos associados, incluindo banners e outros arquivos relevantes.

## API E PAGINAÇÃO

- A documentação da API fica em `/docs`.
- O projeto utilizará paginação com `fastapi-pagination`.
- As consultas devem evitar carregar tabelas inteiras.
- As entidades com relacionamentos serão consultadas com eager loading.
- Os uploads de arquivos serão salvos no sistema de arquivos local da aplicação.

## Seed De Dados

O projeto possui um script de carga para eventos em:

```text
scripts/populate_events.py
```

Ele povoa o banco configurado no `.env` com eventos realistas usando a stack relacional atual.

Exemplo de execução:

```bash
uv run scripts/populate_events.py --count 1000
```

Você também pode fixar a geração com uma seed:

```bash
uv run scripts/populate_events.py --count 1000 --seed 42
```

## Ambiente Local

Copie o arquivo de exemplo de ambiente:

```bash
cp .env.example .env
```

O projeto já deixa duas URLs preparadas no `.env`:

- `sqlite+aiosqlite:///./sqlite_data/eventflow.db` para desenvolvimento local com SQLite
- `postgresql+asyncpg://eventflow:eventflow@localhost:5432/eventflow` para PostgreSQL via Docker

Os logs SQL do `SQLModel/SQLAlchemy` ficam habilitados por exigência do trabalho e podem ser controlados por:

- `SQL_ECHO=true`

Observação: o `SQLite` nao roda como um servico no `docker-compose`, porque ele e apenas um arquivo local. Por isso o `docker-compose.yml` sobe apenas o `PostgreSQL` e o `Adminer`.

## Subir O PostgreSQL Local

```bash
docker compose up -d
```

Servicos disponiveis:

- PostgreSQL em `localhost:5432`
- Adminer em `http://localhost:8080`

## Como Executar

O ponto de entrada atual é `main.py`.

```bash
uv run main.py
```

## Documentação Dos Endpoints

```text
http://localhost:3000/docs
```

## Estado Atual

- O projeto usa `SQLModel` assíncrono com `Alembic`.
- O ambiente local com PostgreSQL via Docker já está configurado.
- O SQLite local também pode ser usado via `.env`.
- Os logs SQL estão habilitados por exigência do trabalho.
