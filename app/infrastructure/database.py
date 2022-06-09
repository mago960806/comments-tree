from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from sqlalchemy.orm import declarative_base


engine = create_engine(
    settings.DATABASE_URI,
    echo=settings.SQL_DEBUG,
    future=True,
)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def create_tables() -> None:
    from app.models import User, Comment

    Base.metadata.create_all(bind=engine)
