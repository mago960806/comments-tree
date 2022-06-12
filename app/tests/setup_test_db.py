from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.infrastructure.database import Base


SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # echo=True,
    future=True,
    # 避免 SQLite3 在多线程环境中出现错误
    connect_args={"check_same_thread": False},
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    bind=engine,
)


def create_tables() -> None:
    Base.metadata.create_all(engine)


def override_get_session() -> Iterator[Session]:
    session: Session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
