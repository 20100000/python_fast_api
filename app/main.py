from fastapi import FastAPI
from app.DB.database import engine, Base
from app.users.router import router as users_router
from app.companies.router import router as companies_router
from app.DB.seeds.run import run_all_seeds
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router

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
# Configuração do CORS para permitir tudo (*)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de teste/saúde da API
@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "API está rodando perfeitamente!"}

# Inclui as rotas e módulos
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(companies_router)
