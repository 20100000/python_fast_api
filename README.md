# 🚀 FastAPI Modular CRUD (Users & Companies)

Uma API RESTful moderna, de alta performance e estruturada de forma modular, desenvolvida com **FastAPI**, **SQLAlchemy 2.0** e **PostgreSQL**. O ambiente é totalmente de nível profissional, contando com isolamento de credenciais via `.env`, segurança nativa com **JWT (JSON Web Tokens)** via *Guards* inspirados no NestJS, e um sistema automatizado de sementes (*Seeds*) para inicialização rápida de dados.

---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.11](https://python.org)** - Linguagem de programação base.
* **[Pytest 8.2.2](https://docs.pytest.org/en/stable/)** - Para teste automático TDD.
* **[FastAPI](https://tiangolo.com)** - Framework web focado em alta performance e documentação automatizada.
* **[SQLAlchemy 2.0](https://sqlalchemy.org)** - ORM robusto para mapeamento das tabelas SQL.
* **[Pydantic v2](https://pydantic.dev)** - Validação de dados de entrada e saída.
* **[Pydantic Settings](https://pydantic.dev)** - Gerenciamento e validação estrita de variáveis de ambiente.
* **[Bcrypt 4.2.0](https://github.com)** - Criptografia nativa e segura para senhas.
* **[PyJWT 2.10.1](https://readthedocs.io)** - Geração e decodificação de Tokens de Acesso.
* **[PostgreSQL 15](https://postgresql.org)** - Banco de dados relacional de produção.
* **[SQLite 3.46.1](https://sqlite.org/)** - Banco de dados usado somente para teste (TDD).
* **[Docker & Docker Compose](https://docker.com)** - Criação de ambientes isolados e orquestração de contêineres.

---

## 📂 Arquitetura do Projeto

O projeto utiliza uma **arquitetura modular por recursos**, facilitando a escalabilidade, manutenção e separação de escopo do código:

```text
meu-projeto-fastapi/
│
├── app/
│   ├── __init__.py
│   ├── main.py             # Ponto de entrada da API e registro de roteadores
│   ├── config.py           # Leitura centralizada e tipada do arquivo .env
│   │
│   ├── auth/               # 🔐 NOVO: Módulo central de Segurança e Criptografia
│   │   ├── __init__.py
│   │   ├── guards.py       # Infraestrutura de Guards estilo NestJS (@router.UseGuards)
│   │   ├── router.py       # Endpoint HTTP de Login (/auth/login)
│   │   └── security.py     # Funções de hashing e validação do token JWT
│   │
│   ├── companies/          # Módulo isolado de Empresas
│   │   ├── __init__.py
│   │   ├── crud.py         
│   │   ├── models.py       
│   │   ├── router.py       # Endpoints protegidos pelos Guards de autenticação
│   │   └── schemas.py      
│   │
│   ├── users/              # Módulo isolado de Usuários
│   │   ├── __init__.py
│   │   ├── models.py       # Inclusão do campo password criptografado
│   │   ├── router.py
│   │   ├── schemas.py      # Filtro para nunca expor senhas em respostas HTTP

|   │   └── services/      
│   │        ├── __init__.py
│   │        ├── create.py  # Intercepta senhas e aplica hash antes de salvar
│   │        ├── delete.py
│   │        ├── exceptions.py
│   │        ├── get.py
│   │        └── update.py  # Lógica centralizada para validação de Usuário Master
│   │
│   └──DB/ 
│       ├── database.py       # Conexão global consumindo a URL do config.py
|       └── seeds/            
│           ├── __init__.py
│           ├── companies_seed.py
│           ├── users_seed.py # Cadastra usuários de teste já criptografando a senha
│           └── run.py          
│ 
├── tests/                  # Suíte de testes automatizados isolados
│   ├── __init__.py
│   ├── conftest.py          
│   └── users/               
│       ├── __init__.py
│       ├── test_create.py
│       ├── test_delete.py
│       ├── test_get_all.py
│       ├── test_get_by_id.py
│       └── test_update.py
│
├── .env                    # Arquivo de configuração de segredos (Ignorado no Git)
├── Dockerfile              
├── docker-compose.yml      # Configuração limpa usando variáveis estruturadas ${}
├── pytest.ini              
└── requirements.txt        
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

   DATABASE_URL=postgresql://tiago:tiago123@db:5432/python_crud
   ```

3. **Inicie os contêineres do Docker:**
   O comando abaixo fará o download do PostgreSQL, aplicará as variáveis de chaves `${}`, instalará as dependências, criará as tabelas de forma automática e rodará as sementes (*Seeds*) de usuários criptografados.
   ```bash
   docker compose up --build
   ```

4. **Acompanhe a inicialização:**
   Aguarde até visualizar a mensagem de sucesso informando que os seeds rodaram e o servidor web está online:
   ```text
   fastapi_app  | Seed: Usuário Tiago Administrador criado com sucesso.
   fastapi_app  | INFO:     Uvicorn running on http://0.0.0 (Press CTRL+C to quit)
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

Para rodar todos os testes de maneira simplificada dentro do ambiente Docker já configurado, lembrado de executar primeiro "docker compose up" utilize o comando:

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
**Próximos passos Prontos para Desenvolvimento**<br/>
* 🗄️ **Migrações de Banco de Dados:** Uso do Alembic para gerenciar alterações e controle de versão na estrutura das tabelas do PostgreSQL de forma profissional.

---

## 👥 Autor

* **Nome:** Tiago Honório
* **Email:** [tiago_honorio2010@hotmail.com](mailto:tiago_honorio2010@hotmail.com)
* **GitHub:** [@20100000](https://github.com/20100000)