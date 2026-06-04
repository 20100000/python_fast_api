from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Chaves de Segurança do JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Strings de Conexão da API
    DATABASE_URL: str

    # 🗄️ Campos Adicionados para resolver o erro 'extra_forbidden'
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
