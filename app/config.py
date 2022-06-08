from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 5000

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
