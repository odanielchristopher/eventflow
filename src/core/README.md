# Core

Esta pasta contém a infraestrutura de persistência usada por todo o projeto.

## Objetivo

`core/` deve ser genérica e focada nos mecanismos do Delta Lake, sem regras de negócio.

## Arquivos

- `client.py`
  - Cria um repositório para cada entidade.
  - Expõe uma API no estilo Prisma, como `client.events` e `client.registrations`.

- `repository.py`
  - Implementa o repositório genérico do Delta Lake.
  - Oferece criação, busca, atualização, exclusão, contagem, vacuum e exportação em lotes.
  - A listagem usa leitura em blocos pequenos e paginação por `limit` e `offset`, sem carregar a tabela inteira na memória.

- `storage.py`
  - Cuida dos caminhos do sistema de arquivos.
  - Gerencia os arquivos `.seq` para IDs auto incrementais.
  - Garante que os diretórios de dados existam.

## Regra Importante

Não coloque regras de aplicação aqui. Esta pasta deve saber apenas como ler e gravar dados no Delta Lake com segurança.
