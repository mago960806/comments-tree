from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    # 数据库配置
    DATABASE_URI: str = "sqlite:///db.sqlite3"
    SQL_DEBUG: bool = False
    # 认证配置
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 一个月

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
