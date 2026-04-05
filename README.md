# EventFlow API

A EventFlow API é um projeto FastAPI que usa Delta Lake como camada de persistência para dados de inscrições, eventos e credenciamento.

## Estrutura Atual

O projeto é organizado em torno de um client no estilo Prisma, que expõe o acesso aos repositórios de cada entidade do domínio.

- `DeltaLakeClient` atua como ponto de entrada da persistência.
- `DeltaLakeRepository` executa as operações reais no Delta Lake.
- `routes/` expõe a API HTTP.
- `usecases/` concentra as regras de negócio.

```text
src/
  core/
    DeltaLakeClient
    DeltaLakeRepository
    helpers de armazenamento
  data/
    tabelas Delta Lake e arquivos .seq
  models/
    entidades de domínio com Pydantic
  routes/
    rotas do FastAPI
  usecases/
    regras de negócio e fluxos
```

## Como As Camadas Se Conectam

1. `routes` recebem a requisição HTTP.
2. `usecases` aplicam as regras de negócio e orquestram o fluxo.
3. `core` lê e grava no Delta Lake.
4. `data` armazena os arquivos físicos.

## API E PAGINAÇÃO

- A documentação da API fica em `/docs` com Scalar.
- No startup, a aplicação informa no log o acesso à documentação.
- `GET /events` aceita `page` e `per_page`.
- Internamente, a listagem é executada em blocos pequenos para evitar carregar tudo na RAM de uma vez.
- Exportações grandes usam streaming.

## Seed De Dados

Para popular o minibanco com dados realistas de eventos:

```bash
uv run scripts/populate_events.py --count 1000
```

Você também pode fixar a geração com uma seed:

```bash
uv run scripts/populate_events.py --count 1000 --seed 42
```

## Como Executar

O ponto de entrada atual é `main.py`.

```bash
uv run main.py
```
# Documentação dos endpoints

```text
http://localhost:3000/docs
```

## Documentação Das Pastas

Cada pasta principal tem seu próprio README:

- [core](src/core/README.md)
- [models](src/models/README.md)
- [routes](src/routes/README.md)
- [usecases](src/usecases/README.md)
- [data](src/data/README.md)
