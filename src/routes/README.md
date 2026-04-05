# Routes

Esta pasta contém os routers do FastAPI.

## Objetivo

As rotas expõem os endpoints HTTP e conectam as requisições aos use cases.

## O que elas devem fazer

- receber os dados da requisição
- validar com Pydantic
- chamar o use case correto
- retornar as respostas

## Exemplo

- `event.py` define os endpoints relacionados a eventos.
