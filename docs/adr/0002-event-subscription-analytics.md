# ADR 0002 - Analytics de Event e Subscription com MongoDB

## Status

Aceito

## Contexto

O trabalho exige consultas com agregação e filtragem usando MongoDB. O projeto já possui `Event` e `Subscription` em Mongo/Beanie, então a solução precisa expor queries analíticas reais sem misturar seus contratos com os endpoints paginados de CRUD.

## Decisões

- As agregações são expostas por endpoints dedicados em vez de serem embutidas nas listagens de CRUD.
- A contagem de check-ins por evento usa pipeline de aggregation do MongoDB.
- A taxa de presença por evento retorna um valor numérico entre `0` e `1`.
- A contagem total de eventos aceita filtros opcionais por data, localização e título.
- A consulta por faixa de preço usa `min_price` e `max_price` explícitos.

## Consequências

- Os contratos de analytics ficam mais claros no OpenAPI.
- O repositório passa a ter métodos analíticos específicos, separados das buscas paginadas.
- A API fica alinhada com a exigência acadêmica de demonstrar aggregation pipeline.
