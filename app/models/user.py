from datetime import datetime

from sqlalchemy import Boolean, Column, String, Integer, DateTime

from app.infrastructure.database import Base


class User(Base):
    """
    用户模型
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"
