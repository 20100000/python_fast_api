# 🚀 FastAPI Modular CRUD (Users, Companies & Products)

Uma API empresarial moderna, de alta performance e estruturada de forma modular, desenvolvida com **FastAPI**, **SQLAlchemy 2.0**, **Strawberry GraphQL** e **PostgreSQL**. O ambiente conta com isolamento de credenciais via `.env`, segurança nativa com **JWT (JSON Web Tokens)**, versionamento de banco com **Alembic**, e um sistema automatizado de sementes (*Seeds*) para inicialização rápida de dados.

## ⚡ Novidade: Arquitetura Assíncrona Integrada (Rota Users V2)
O projeto conta com o **versionamento de rotas (V2)** para o recurso de Usuários. Esta implementação introduz o modelo de concorrência assíncrona nativa com `async/await` e `AsyncSession` através do driver `asyncpg` para alta performance e escalabilidade de I/O.

## 🍇 Novidade V3: Camada Enterprise com Strawberry GraphQL
A **versão 3 (V3)** da API eleva a arquitetura do projeto ao padrão corporativo ao introduzir o **GraphQL** por meio do ecossistema **Strawberry**.
* **Single Endpoint:** Toda a comunicação, consultas e mutations ocorrem sob o endpoint unificado `/v3/graphql`.
* **Segurança por Guards Globais:** Proteção nativa de queries e mutations usando herança de permissões (`BasePermission`), desacoplando o código de validação repetitivo dos controladores.
* **Services Dedicados (V3/Services):** Camada isolada e especializada de regras de negócio assíncronas para atender estritamente ao ecossistema GraphQL.

---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.11](https://python.org)** - Linguagem de programação base.
* **[FastAPI](https://tiangolo.com)** - Framework web de alta performance e documentação automatizada.
* **[Strawberry GraphQL](https://strawberry.rocks)** - Biblioteca baseada em dataclasses para criação de APIs GraphQL robustas e tipadas.
* **[SQLAlchemy 2.0](https://sqlalchemy.org)** - ORM robusto com suporte assíncrono via `ext.asyncio`.
* **[asyncpg](https://github.com)** - Driver de banco de dados assíncrono e nativo para PostgreSQL.
* **[Alembic 1.13](https://alembic.sqlalchemy.org)** - Controle e versionamento de alterações do banco de dados.
* **[Pydantic v2](https://pydantic.dev)** - Validação estrita de dados de entrada e saída.
* **[Pydantic Settings](https://pydantic.dev)** - Gerenciamento de variáveis de ambiente.
* **[PyJWT 2.10.1](https://pyjwt.readthedocs.io)** - Geração e decodificação de Tokens de Acesso.
* **[PostgreSQL 15](https://postgresql.org)** - Banco de dados relacional de produção.
* **[SQLite 3.46.1](https://sqlite.org/)** - Banco de dados usado somente para testes (TDD).
* **[Docker & Docker Compose](https://docker.com)** - Criação de ambientes isolados e orquestração de contêineres.

---

## 📂 Arquitetura do Projeto

O projeto utiliza uma **arquitetura modular por recursos**, facilitando a escalabilidade, manutenção e separação de escopo do código:

```text
meu-projeto-fastapi/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada da API e registro de roteadores (V1, V2 e V3)
│   ├── config.py           # Leitura centralizada e tipada do arquivo .env
│   ├── graphql_app.py      # Agregador central e unificador de Queries/Mutations do GraphQL V3
│   │
│   ├── auth/               # 🔐 Módulo central de Segurança e Criptografia
│   │   ├── __init__.py
│   │   ├── graphql_guards.py # Guards de Permissão e Validação do JWT para o GraphQL
│   │   ├── router.py       # Endpoint HTTP de Login REST (/auth/login)
│   │   └── security.py     # Funções de hashing e validação do token JWT
│   │
│   └── api/
│       ├── companies/      # Módulo isolado de Empresas (V1, V2)
│       │   ├── __init__.py
│       │   ├── crud.py         
│       │   ├── models.py       
│       │   ├── router.py       
│       │   └── schemas.py   
│       │   └── v2/             
│       │       ├── __init__.py
│       │       ├── router.py  
│       │       └── services/  
│       │
│       ├── products/       # 📦 Módulo isolado de Produtos
│       │   ├── __init__.py
│       │   ├── services/       
│       │   ├── models.py       
│       │   └── router.py       
│       │   └── schemas.py      
│       │
│       └── users/          # Módulo isolado de Usuários
│           ├── __init__.py
│           ├── models.py       
│           ├── router.py       
│           ├── schemas.py      
│           ├── services/       # Services Síncronos V1
│           │
│           ├── v2/             # Submódulo Assíncrono REST (V2)
│           │
│           └── v3/             # 🍇 NOVO: Submódulo Corporativo GraphQL (V3)
│               ├── __init__.py
│               ├── mutations.py  # Controladores de escrita do GraphQL (Create, Update, Delete)
│               ├── queries.py    # Controladores de leitura do GraphQL (Queries)
│               ├── types.py      # Mapeadores e Inputs de dados do Strawberry
│               └── services/     # Camada de regras de negócio assíncronas EXCLUSIVA da V3
│                   ├── __init__.py
│                   ├── create.py
│                   ├── delete.py
│                   ├── get.py
│                   └── update.py
│        
│   └── DB/ 
│       ├── database.py     # Conexão global suportando Session síncrona e AsyncSession Local
│       ├── migrations/     # Histórico e scripts de migração do Alembic
│       └── seeds/          # Alimentação automática inicial do banco de dados
```

---

## 🚀 Como Iniciar a Aplicação

### Pré-requisitos
Certifique-se de ter instalado em sua máquina:
* [Git](https://git-scm.com)
* [Docker & Docker Compose](https://docker.com)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/20100000/python_fast_api.git
   cd python_fast_api
   ```

2. **Configure o arquivo `.env`:**
   Crie um arquivo chamado `.env` na raiz do projeto (ao lado do `docker-compose.yml`) e preencha com as suas chaves e dados de banco:
   ```env
   SECRET_KEY=sua_chave_secreta_super_longa_e_segura_de_producao_123!
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60

   POSTGRES_USER=tiago
   POSTGRES_PASSWORD=tiago123
   POSTGRES_DB=python_crud

   DATABASE_URL=postgresql+asyncpg://tiago:tiago123@db:5432/python_crud
   ```

3. **Inicie os contêineres do Docker:**
   O comando abaixo fará o download do PostgreSQL, aplicará as variáveis de chaves, instalará as dependências (`requirements.txt`) e subirá o servidor automaticamente:
   ```bash
   docker compose down
   docker compose up --build
   ```

---

## 🍇 Como consumir a API GraphQL V3

A interface interativa do **Strawberry (GraphiQL)** fica disponível publicamente em: `http://localhost:8000/v3/graphql`.

### 🔐 Autenticação nas Requisições
Para executar as queries ou mutations que possuem proteção por **Guard**, você deve obter seu Token JWT no endpoint `/auth/login` (via REST) e adicioná-lo no rodapé do painel do GraphiQL na aba **Headers** usando o formato JSON abaixo:

```json
{
  "Authorization": "Bearer SEU_TOKEN_JWT_AQUI"
}
```

### 📑 Exemplos Práticos de Operações

#### 1. Query: Listar Usuários (Requer Token)
```graphql
query {
  allUsers(skip: 0, limit: 10) {
    id
    name
    email
    admin
    createdAt
    updatedAt
  }
}
```

#### 2. Mutation: Criar Novo Usuário (Público)
```graphql
mutation {
  createUser(input: {
    name: "John Doe",
    email: "john@example.com",
    password: "securepassword123",
    admin: false
  }) {
    id
    name
    email
    createdAt
  }
}
```

#### 3. Mutation: Atualizar Dados do Usuário (Requer Token)
```graphql
mutation {
  updateUser(userId: 1, input: {
    name: "John Doe Alterado",
    admin: true
  }) {
    id
    name
    admin
    updatedAt
  }
}
```


4. **Acompanhe a inicialização:**
   Aguarde até visualizar a mensagem de sucesso informando que os seeds rodaram e o servidor web está online:
   ```text
   fastapi_app  | Seed: Usuário Tiago Administrador criado com sucesso.
   fastapi_app  | INFO:     Uvicorn running on http://0.0.0 (Press CTRL+C to quit)
   ```

---

## 🔄 Migrações com Alembic (Docker)

O versionamento estrutural do banco de dados (PostgreSQL) é controlado via Alembic. Toda modificação em arquivos `models.py` deve ser acompanhada do fluxo abaixo utilizando o contêiner `web`:

### 1. Criar script de migrate
Compare as suas classes de model atuais com o estado do banco e gere de forma automática o arquivo com as alterações na pasta `versions/`:
```bash
docker compose run --rm web alembic revision --autogenerate -m "create_products_table"
```

### 2. Enviar para o banco de dados
Para rodar as atualizações estruturais pendentes e criar efetivamente as tabelas e colunas correspondentes dentro do banco PostgreSQL, execute:
```bash
docker compose run --rm web alembic upgrade head
```

---

## 🔒 Autenticação & Como Testar via Swagger UI

A API possui rotas protegidas que impedem acessos anônimos, utilizando decoradores avançados baseados em *Guards* estilo NestJS (`@router.UseGuards(JwtAuthGuard)`). Para testar o ecossistema completo autenticado, siga o passo a passo:

1. Abra o navegador em: **[http://localhost:8000/docs](http://localhost:8000/docs)**
2. Você notará um botão global chamado **"Authorize"** com o ícone de um cadeado no topo direito, e pequenos cadeados ao lado das rotas privadas (como `GET /companies/`).
3. **Efetuando o Login no Sistema:**
   * Clique no botão global **"Authorize"** no topo da página.
   * Uma janela de formulário nativo vai se abrir.
   * No campo **username**, digite o e-mail criado pelo seed: `admin@gmail.com`
   * No campo **password**, digite a senha padrão: `test`
   * Deixe os campos *client_id* e *client_secret* vazios e clique no botão **Authorize**.
   * Clique em *Close*. O cadeado global ficará **trancado e verde**.
4. **Testando as Rotas Protegidas:**
   * Com o cadeado trancado, expanda a rota `GET /companies/` ou `GET /users/{user_id}`.
   * Clique em **"Try it out"** e depois em **"Execute"**.
   * O Swagger injetará automaticamente o cabeçalho `-H 'Authorization: Bearer <token>'` nos bastidores e trará os dados com sucesso (`200 OK`). O token carregará no seu payload decodificado o e-mail (`sub`), o `name` e o `id` do usuário logado.

---

## 🧪 Testes Automatizados & TDD (Coverage)

A suíte de testes utiliza **Pytest** integrado a um banco **SQLite em memória (`sqlite:///:memory:`)**. Isso garante o isolamento total dos testes sem corromper ou sujar os dados do banco PostgreSQL de desenvolvimento, permitindo fluxos rápidos de TDD.

### Como Executar os Testes

Para rodar todos os testes de maneira simplificada dentro do ambiente Docker já configurado, lembrando de executar primeiro `docker compose up`, utilize o comando:

```bash
docker compose run --rm web pytest
```

### Comandos Úteis para Desenvolvimento Modular (TDD)

* **Executar apenas o arquivo de criação de usuários (Foco em TDD):**
  ```bash
  docker compose run --rm web pytest tests/users/test_create.py
  ```
* **Aumentar o detalhamento das asserções executadas:**
  ```bash
  docker compose run --rm web pytest -v
  ```

---

## 🔄 Integração Contínua Automatizada (CI/CD Pipeline)

O projeto conta com uma esteira de **Integração Contínua (CI)** totalmente automatizada via **GitHub Actions** (configurada em `.github/workflows/ci.yml`).

Toda vez que um novo código é enviado (`git push`) ou um **Pull Request (PR)** é aberto para a branch principal (`main`), o GitHub dispara automaticamente um gatilho que executa os seguintes passos em um servidor isolado:

1. **Setup do Ambiente:** Instalação do Python 3.11 com gerenciamento inteligente de cache para acelerar o processo.
2. **Isolamento de Configurações:** Criação dinâmica de um arquivo `.env` temporário de testes para satisfazer as validações de inicialização do `Pydantic Settings`.
3. **Instalação de Dependências:** Instalação limpa de todos os pacotes do `requirements.txt`.
4. **Validação de Código (Pytest):** Execução automatizada da suíte completa de testes baseada em **SQLite em memória**.

> 🛡️ **Garantia de Qualidade:** Se qualquer teste falhar ou quebrar as regras dos *JWT Guards*, a esteira ficará vermelha e o GitHub bloqueará automaticamente o merge do código na branch de produção até que o bug seja corrigido.

---

## 👥 Autor

* **Nome:** Tiago Honório
* **Email:** [tiago_honorio2010@hotmail.com](mailto:tiago_honorio2010@hotmail.com)
* **GitHub:** [@20100000](https://github.com/20100000)