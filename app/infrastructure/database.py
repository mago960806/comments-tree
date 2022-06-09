from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from app.config import settings

engine = create_engine(
    settings.DATABASE_URI,
    echo=settings.SQL_DEBUG,
    future=True,
    # 避免 SQLite3 在多线程环境中出现错误
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    bind=engine,
)

Base = declarative_base()


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
