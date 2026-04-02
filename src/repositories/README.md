# Repositories

Esta pasta é destinada aos repositórios da aplicação.

## Objetivo

Esses repositórios ficam acima de `core/` e adaptam o Delta Lake client às necessidades da aplicação.

## O que entra aqui

- `EventsRepo`
- `RegistrationsRepo`
- `SpeakersRepo`
- `ActivitiesRepo`
- `CheckInsRepo`

## Responsabilidade

- centralizar o acesso à persistência por caso de uso
- esconder chamadas diretas ao `DeltaLakeClient`
- aplicar filtros padrão ou padrões de consulta quando necessário

## Regra Importante

As regras de negócio devem ficar em `usecases/`, não aqui.
