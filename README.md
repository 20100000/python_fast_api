# 🚀 FastAPI Modular CRUD (Users & Companies)

Uma API RESTful moderna, de alta performance e estruturada de forma modular, desenvolvida com **FastAPI**, **SQLAlchemy 2.0** e **PostgreSQL**. O ambiente é totalmente conteinerizado utilizando **Docker** e **Docker Compose**, contando com um sistema automatizado de sementes (*Seeds*) para inicialização rápida de dados.

---

## 🛠️ Tecnologias Utilizadas

* **[Python 3.11](https://python.org)** - Linguagem de programação base.
* **[FastAPI](https://tiangolo.com)** - Framework web focado em alta performance e documentação automatizada.
* **[SQLAlchemy 2.0](https://sqlalchemy.org)** - ORM robusto para mapeamento das tabelas SQL.
* **[Pydantic v2](https://pydantic.dev)** - Validação de dados de entrada e saída.
* **[PostgreSQL 15](https://postgresql.org)** - Banco de dados relacional de produção.
* **[Docker & Docker Compose](https://docker.com)** - Criação de ambientes isolados e orquestração de contêineres.

---

## 📂 Arquitetura do Projeto

O projeto utiliza uma **arquitetura modular por recursos**, facilitando a escalabilidade, manutenção e separação de escopo do código:

```text
meu-projeto-fastapi/
│
├── app/
│   ├── __init__.py
│   ├── database.py         # Configuração de conexão global com o banco de dados
│   ├── main.py             # Ponto de entrada da API e registro de rotas
│   │
│   ├── companies/          # Módulo isolado de Empresas
│   │   ├── __init__.py
│   │   ├── crud.py         # Operações de banco de dados (Query/Insert/Delete)
│   │   ├── models.py       # Modelo da tabela do SQLAlchemy
│   │   ├── router.py       # Endpoints HTTP da API
│   │   └── schemas.py      # Esquemas de validação do Pydantic
│   │
│   ├── users/              # Módulo isolado de Usuários
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── models.py
│   │   ├── router.py
│   │   └── schemas.py
│   │
│   └── seeds/              # Gerenciamento escalável de Seeds automáticos
│       ├── __init__.py
│       ├── companies_seed.py
│       ├── users_seed.py
│       └── run.py          # Orquestrador geral de execução dos seeds
│
├── Dockerfile              # Configuração do contêiner da aplicação Python
├── docker-compose.yml      # Orquestração do FastAPI + PostgreSQL + Healthcheck
└── requirements.txt        # Dependências do ecossistema Python
```

---

## 🚀 Como Iniciar a Aplicação

### Pré-requisitos
Certifique-se de ter instalado em sua máquina:
* [Git](https://git-scm.com)
* [Docker & Docker Compose](https://docker.comproducts/docker-desktop/)

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd SEU_REPOSITORIO
   ```

2. **Inicie os contêineres do Docker:**
   O comando abaixo fará o download do PostgreSQL, instalará as dependências do Python, criará as tabelas de forma automática e aplicará as sementes de dados iniciais.
   ```bash
   docker compose up --build
   ```

3. **Acompanhe a inicialização:**
   Aguarde até visualizar a mensagem de sucesso no terminal informando que o servidor web está online:
   ```text
   fastapi_app  | INFO:     Uvicorn running on http://0.0.0 (Press CTRL+C to quit)
   ```

---

## 🧪 Como Testar pelo Swagger UI

O FastAPI gera uma documentação interativa fantástica por padrão. Para testar o CRUD completo (Users e Companies), siga os passos:

1. Abra o seu navegador e acesse: **[http://localhost:8000/docs](http://localhost:8000/docs)**
2. Você verá as rotas separadas de forma organizada por blocos (`users`, `companies` e `Health Check`).
3. **Testando uma Rota (Exemplo: Listar Usuários):**
   * Clique em `GET /users/`.
   * Clique no botão **"Try it out"** no canto direito.
   * Clique no botão azul **"Execute"**.
   * O Swagger mostrará a resposta real retornada pelo PostgreSQL, contendo inclusive os dados pré-carregados pelos *Seeds* automatizados com suas respectivas datas de criação e atualização.
4. **Testando uma Criação (Exemplo: Nova Empresa):**
   * Clique em `POST /companies/`.
   * Clique em **"Try it out"**.
   * Altere os dados no JSON do campo de texto informando o nome e o CNPJ desejados.
   * Clique em **"Execute"** para efetivar o cadastro no banco.

---

## 👥 Autor

* **Nome:** Tiago Honório
* **Email:** [tiago_honorio2010@hotmail.com](mailto:tiago_honorio2010@hotmail.com)
* **GitHub:** [@SEU_USUARIO](https://github.com)

---
Desenvolvido para fins de aprendizado de boas práticas em arquitetura de microsserviços com Python. 🌟
