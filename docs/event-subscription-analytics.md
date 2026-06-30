# Event e Subscription Analytics

## Endpoints

### `GET /events/{event_id}/subscriptions/analytics/check-ins/count`

- Objetivo: contar quantas inscrições de um evento possuem check-in registrado.
- Resposta:
```json
{ "count": 12 }
```
- Exigência coberta: quantidade total de registros relacionados com filtro por evento.

### `GET /events/{event_id}/subscriptions/analytics/attendance-rate`

- Objetivo: calcular a taxa de presença de um evento.
- Resposta:
```json
{
  "event_id": "685f...",
  "subscriptions_count": 20,
  "check_ins_count": 12,
  "attendance_rate": 0.6
}
```
- Exigência coberta: agregação com filtro e cálculo derivado.

### `GET /events/analytics/count`

- Objetivo: contar o total de eventos cadastrados.
- Filtros:
  - `date_from`
  - `date_to`
  - `location`
  - `title`
  - `case_sensitive`
- Resposta:
```json
{ "count": 8 }
```
- Exigência coberta: quantidade total de documentos cadastrados com filtros opcionais.

### `GET /events/analytics/by-subscription-price-range`

- Objetivo: listar eventos dentro de uma faixa de preço de inscrição.
- Filtros:
  - `min_price`
  - `max_price`
  - `date_from`
  - `date_to`
  - `location`
  - `title`
  - `case_sensitive`
  - `page`
  - `size`
- Resposta: `Page[EventRead]`, incluindo `documents`.
- Exigência coberta: consulta filtrada por atributo numérico com critérios adicionais.
