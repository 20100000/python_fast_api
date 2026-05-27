from app.DB.database import SessionLocal
from app.DB.seeds.users_seed import seed_users
from app.DB.seeds.companies_seed import seed_companies

def run_all_seeds():
    db = SessionLocal()
    try:
        print("🚀 Iniciando a inserção de sementes (Seeds) no banco de dados...")
        
        # Executa a função de semente de cada módulo
        seed_users(db)
        seed_companies(db)  
        # seed_products(db) <- Exemplo para o futuro
        
        print("✅ Todas as sementes foram processadas.")
    except Exception as e:
        print(f"❌ Erro ao rodar os seeds: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_all_seeds()
