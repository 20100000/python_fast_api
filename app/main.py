from fastapi import FastAPI
from app.database import engine, Base
from app.users.router import router as users_router
from app.companies.router import router as companies_router
from app.users import models 
from app.companies import models as company_models
from app.seeds.run import run_all_seeds

# 1. Cria as tabelas no banco de dados automaticamente se não existirem
Base.metadata.create_all(bind=engine)

# 2. Executa os seus múltiplos seeds de forma automatizada
run_all_seeds()

# 3. Inicializa o FastAPI mantendo o Swagger customizado ativo
app = FastAPI(
    title="🚀 User Management API",
    description="""
    API robusta para gerenciamento e cadastro.
    """,
    version="1.0.0",
    contact={
        "name": "Tiago Honorio",
        "email": "tiago_honorio2010@hotmail.com",
    },
    docs_url="/docs", 
    redoc_url="/redoc"
)

# Rota de teste/saúde da API
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "API está rodando perfeitamente!"}

# Inclui as rotas do módulo de usuários
app.include_router(users_router)
app.include_router(companies_router)
