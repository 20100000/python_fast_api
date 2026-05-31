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
│   │   ├── models.py
│   │   ├── router.py
│   │   └── schemas.py

|   │   └── services/      # Operações de banco de dados divididas por scripts com responsabilidade única
│   │        ├── __init__.py
│   │        ├── create.py
│   │        ├── delete.py
│   │        ├── exceptions.py
│   │        ├── get.py
│   │        └── update.py   
│   │
│   └──DB/ 
│       ├── database.py       # Configuração de conexão global com o banco de dados
|       └── seeds/            # Gerenciamento escalável de Seeds automáticos
│           ├── __init__.py
│           ├── companies_seed.py
│           ├── users_seed.py
│           └── run.py          # Orquestrador geral de execução dos seeds
│ 
├── tests/                  # Suíte de testes automatizados isolados
│   ├── __init__.py
│   ├── conftest.py          # Configurações globais e fixtures do SQLite em memória
│   └── users/               # Módulos de testes focados em usuários (TDD)
│       ├── __init__.py
│       ├── test_create.py
│       ├── test_delete.py
│       ├── test_get_all.py
│       ├── test_get_by_id.py
│       └── test_update.py
│
├── Dockerfile              # Configuração do contêiner da aplicação Python
├── docker-compose.yml      # Orquestração do FastAPI + PostgreSQL + Healthcheck
├── pytest.ini              # Regras de execução e silenciamento de warnings do Pytest
└── requirements.txt        # Dependências do ecossistema Python
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

## 🧪 Testes Automatizados & TDD (Coverage)

A suíte de testes utiliza **Pytest** integrado a um banco **SQLite em memória (`sqlite:///:memory:`)**. Isso garante o isolamento total dos testes sem corromper ou sujar os dados do banco PostgreSQL de desenvolvimento, permitindo fluxos rápidos de TDD.

### Como Executar os Testes

Para rodar todos os testes de maneira simplificada dentro do ambiente Docker já configurado, utilize o comando:

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

### Métrica de Cobertura de Código (% Coverage)

O projeto conta com o **`pytest-cov==7.1.0`** configurado diretamente no arquivo `pytest.ini`. Toda vez que os testes rodam, uma tabela de cobertura de scripts é impressa no terminal, apontando quais caminhos e linhas exatas do código não foram validados:

```text
---------- coverage: platform linux, python 3.11.15-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/__init__.py                     0      0   100%
app/main.py                        13      2    85%   11-12
app/users/router.py                20      0   100%
app/users/services/create.py       18      0   100%
-------------------------------------------------------------
TOTAL                              95      2    97%
```

---

## 🌐 Como Testar pelo Swagger UI

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
* **GitHub:** [@20100000](https://github.com/20100000)

---
Desenvolvido para fins de aprendizado de boas práticas em arquitetura de microsserviços com Python. 🌟
