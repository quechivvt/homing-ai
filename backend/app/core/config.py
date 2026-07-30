from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Setting(BaseSettings):

    # LLM Model
    GEMINI_API_KEY: str
    GEMINI_MODEL:str
    EMBEDDING_MODEL:str
    BASE_URL:str="https://generativelanguage.googleapis.com/v1beta/openai/"

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Pipeline
    PIPELINE:str

    # Redis
    REDIS_URL:str

    # Retriver Config
    MAX_DISTANCE : float

    # Load .env
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
settings = Setting()