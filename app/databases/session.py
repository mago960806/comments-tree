from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings


engine = create_engine(settings.DATABASE_URI, echo=settings.SQL_DEBUG, future=True)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
