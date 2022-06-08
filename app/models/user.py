from sqlalchemy import Boolean, Column, String

from app.databases import BaseModel


class User(BaseModel):
    """
    用户模型
    """

    username = Column(String(20), unique=True, index=True, nullable=False)
    password = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=True)

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r})"
