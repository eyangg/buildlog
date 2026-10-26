from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    debug: bool = False
    secret_key: str
    algorithm: str = "HS256"
    database_url: str = "sqlite:///./database.db"
    access_token_expire_minutes: int = 30


settings = Settings()
