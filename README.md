# EventFlow API

A EventFlow API é um projeto FastAPI que usa Delta Lake como camada de persistência para dados de inscrições, eventos e credenciamento.

## Estrutura Atual

O projeto é organizado em torno de um client no estilo Prisma, que expõe o acesso aos repositórios de cada entidade do domínio.

- `DeltaLakeClient` atua como ponto de entrada da persistência.
- `DeltaLakeRepository` executa as operações reais no Delta Lake.
- `routes/` expõe a API HTTP.
- `usecases/` concentra as regras de negócio.
- `repositories/` concentra os repositórios da aplicação que usam o core.

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
  repositories/
    repositórios da aplicação
  routes/
    rotas do FastAPI
  usecases/
    regras de negócio e fluxos
```

## Como As Camadas Se Conectam

1. `routes` recebem a requisição HTTP.
2. `usecases` aplicam as regras de negócio e orquestram o fluxo.
3. `repositories` conversam com o `DeltaLakeClient`.
4. `core` lê e grava no Delta Lake.
5. `data` armazena os arquivos físicos.

## Observações de Desenvolvimento

- Mantenha os identificadores do código em inglês.
- Não coloque regra de negócio nas rotas do FastAPI.
- Não carregue a tabela inteira na memória.
- Prefira leitura em lotes ou streaming para paginação e exportação.

## Como Executar

O ponto de entrada atual é `main.py`.

```bash
uv run main.py
```

Se o ambiente estiver configurado com a virtualenv do projeto, isso inicia a aplicação FastAPI com Uvicorn.

## Documentação Das Pastas

Cada pasta principal tem seu próprio README:

- [core](src/core/README.md)
- [models](src/models/README.md)
- [repositories](src/repositories/README.md)
- [routes](src/routes/README.md)
- [usecases](src/usecases/README.md)
- [data](src/data/README.md)
