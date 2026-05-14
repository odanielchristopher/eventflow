Trabalho Prático: Implementação de API Web com FastAPI e SQLModel
Objetivo
Desenvolver uma API Web para gerenciar as entidades definidas no Trabalho Prático 0, implementando operações CRUD e consultas complexas.

Requisitos Técnicos
Tecnologias
FastAPI para construção da API
SQLModel para persistência de dados (integrando SQLAlchemy e Pydantic)
Suporte para SQLite e PostgreSQL
UV como gerenciador de dependências
Estrutura do Projeto
Organização modular com separação clara de responsabilidades:

Models (entidades)
Rotas (endpoints)
Configurações em arquivo(s) externo(s) à aplicação (.env)
Migrações (Alembic)
etc.
Requisitos de Implementação
1. Mínimo de 5 entidades com relacionamentos entre si
2. Deve ter pelo menos um relacionamento one-to-many/many-to-one e pelo menos um relacionamento many-to-many. Relacionamento one-to-one é opcional. 
3. Implementação completa de operações CRUD para todas as entidades
4. Tratamento robusto de exceções para garantir resiliência da aplicação. As exceções devem ser tratadas adequadamente para evitar falhas abruptas na aplicação.
5. Documentação dos endpoints via OpenAPI/Swagger
6. Nunca carregue a tabela inteira: aplique sempre paginação e/ou filtros ao consultar o banco para evitar trazer muitos dados de uma só vez. Use a biblioteca fastapi-pagination para realizar a paginação dos dados.
7. Persistência: use a API ORM do SQLModel. Ao consultar entidades com relacionamentos, utilize eager loading com joinedload() ou selectinload(), evitando lazy loading. 
selectinload() é geralmente a melhor estratégia para coleções one-to-many e many-to-many, enquanto joinedload() é mais adequado para relações many-to-one e one-to-one.
8. Usar a API assíncrona no SQLModel e Alembic. Mais detalhes em: FastAPI with Async SQLAlchemy, SQLModel, and Alembic. O que muda de fato entre síncrono e assíncrono?
def → async def;
Session → AsyncSession;
Engine → AsyncEngine;
create_engine → create_async_engine;
driver sync → driver async, como asyncpg;
chamadas diretas → chamadas com await;
testes sync → testes async;
repositórios/services sync → repositórios/services async.
7. A aplicação deve permitir que pelo menos uma entidade tenha um ou mais documentos associados. 
Os documentos podem ser imagens ou arquivos PDF. 
O conteúdo do arquivo não deve ser armazenado no banco de dados. 
O arquivo deve ser salvo no sistema de arquivos local da aplicação.
O banco de dados deve armazenar apenas os metadados do documento.
A aplicação deve possuir uma entidade específica (Document) para representar os metadados dos arquivos.
A entidade Document deve possuir, no mínimo, os seguintes atributos:
id: identificador do documento;
original_filename: nome original enviado pelo usuário;
content_type: tipo MIME do arquivo;
extension: extensão do arquivo;
size_bytes: tamanho do arquivo em bytes;
created_at: data e hora do envio.
O identificador id do documento deve ser usado pela aplicação para definir o nome físico do arquivo salvo.
A pasta-base de uploads deve ser definida na aplicação.
Deve haver endpoints para inserir, listar ou remover documentos de uma entidade. Exemplo:
POST - /produtos/{produto_id}/documents - Envia um novo documento para o produto
GET - /produtos/{produto_id}/documents - Lista os documentos do produto
GET - /documents/{document_id} - Retorna os metadados do documento
GET - /documents/{document_id}/download - Baixa ou exibe o arquivo
PUT - /documents/{document_id} - Substitui o arquivo do documento
DELETE - /documents/{document_id} - Remove o documento e o arquivo físico
Consultas Requeridas
A API deve implementar consultas diversificadas e úteis para o contexto escolhido.

a) Consultas por ID
b) Listagens filtradas por relacionamentos
c) Buscas por texto parcial
d) Filtros por data/ano
e) Agregações e contagens
f) Classificações e ordenações
g) Consultas complexas envolvendo múltiplas entidades
Exemplos de consultas para um contexto fictício envolvendo Filmes e Atores:

a) Obter ator e filme a partir de seus respectivos ids, sendo uma busca separada para cada um deles.
b) Listar todos os títulos de filmes de um determinado ator.
c) Listar os nomes de todos os atores de um determinado filme.
d) Listar os títulos de filmes lançados em determinado ano.
e) Listar os títulos de filmes cujo título contém determinada string.
f) Listar os nomes de atores nascidos em determinado ano.
g) Mostrar a quantidade total de filmes cadastrados.
h) Mostrar a quantidade total de filmes cadastrados por categoria.
i) Mostrar a quantidade de atores por filme.
j) Mostrar filmes com classificação IMDB (notas de 1 a 10) acima de determinado valor.
Requisitos de Entrega
1. Gestão do Projeto: utilize o uv como ferramenta de gerenciamento do projeto e dependências. Certifique-se de incluir os seguintes arquivos no projeto a ser enviado:

.env - deve ter as URLs de acesso aos bancos SQLite e PostgreSQL (uma delas deve estar ativa e a outra deve estar comentada).
.python-version
uv.lock
pyproject.toml com dependências
migrations do Alembic - toda a criação de tabelas deve ser gerenciada pelo Alembic
2. Banco SQLite e PostgreSQL povoados com dados realistas:

Crie um script Python que popule o minibanco com no mínimo 100 registros por entidade, com dados realistas. Sugestão: utilize a biblioteca Faker com localização pt_BR. O script deve acessar o banco configurado no .env.
Dados consistentes e significativos
Usar PostgreSQL em nuvem (Supabase, Neon ou outro) com credenciais enviadas no arquivo .env. O .env deve conter as credenciais de acesso para SQLite e PostgreSQL, sendo que uma delas deve estar comentada.
A aplicação deve funcionar em qualquer um dos 2 bancos (SQLite e PostgreSQL), bastando mudar a URL de conexão no arquivo .env.
3. Envie apenas o código-fonte, o script de carga e o arquivo do SQLite local já com dados. Não inclua arquivos ou pastas desnecessários (ex.: .venv, __pycache__, .git, etc.). Inclua o arquivo pyproject.toml com as dependências do projeto.

Dicas de Desenvolvimento
Implementar paginação nas listagens
Documentar o projeto usando docstrings
OBSERVAÇÕES:
1. O trabalho deve ser feito em tripla. Não necessariamente precisa ser a mesma tripla do Trabalho Prático 1. Caso a tripla tenha mudado, é necessário submeter novamente o formulário https://forms.gle/Jbb3RifgqkmjCWmT6

2. Crie um arquivo (divisao_tarefas.txt) detalhando a divisão de tarefas e mostrando o que cada membro da dupla efetivamente fez no trabalho. Divida as tarefas definidas entre os membros da dupla. O arquivo deve ser enviado junto com o trabalho.

3. Somente um dos membros da dupla deve enviar o trabalho no Moodle.

4. A apresentação do trabalho é OBRIGATÓRIA E PRESENCIAL para cada membro da tripla, sendo 5 minutos o tempo para cada membro falar. Se algum membro não apresentar o trabalho, ficará com nota ZERO. Não será permitida a apresentação remota. A nota pode variar entre os membros da dupla, dependendo da apresentação e das atividades realizadas no trabalho.

5. Envie dados o mais próximos possível de dados reais. Evite, de todo modo, preencher um atributo com o valor "sadfadsfasdfasd", por exemplo. 

6. Envie o projeto em formato zip pelo Moodle. Não será aceito o envio de link de acesso ao projeto.