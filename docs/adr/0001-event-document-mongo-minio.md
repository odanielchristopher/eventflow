# ADR 0001 - Event e Document com MongoDB + MinIO

## Status

Aceito

## Contexto

O trabalho exige que os metadados dos documentos sejam persistidos no MongoDB e que o arquivo físico seja armazenado no MinIO. O projeto já havia migrado parte das entidades para Mongo, mas `Document` ainda estava em `SQLModel` e o upload usava disco local.

## Decisões

- `Document.event_id` é a única fonte de verdade da associação com `Event`.
- O arquivo físico do documento é armazenado no MinIO; o Mongo guarda apenas os metadados.
- O nome físico do objeto segue o padrão `<document_id>.<extension>`.
- `banner_img_url` continua pertencendo a `Event`.
- Upload de documento de imagem atualiza `banner_img_url` para `/documents/{document_id}/download`.
- Upload de PDF não atualiza `banner_img_url`.
- Se o documento removido ou substituído era o banner atual, `banner_img_url` é limpo.
- O download público da aplicação continua mediado pela API em `/documents/{document_id}/download`, sem expor URL interna do MinIO.

## Consequências

- O relacionamento `Event -> documents` passa a ser resolvido por consulta, evitando redundância.
- O projeto passa a depender da biblioteca `minio`.
- `UPLOAD_DIR` deixa de ser parte funcional do fluxo principal e permanece apenas como legado temporário.
