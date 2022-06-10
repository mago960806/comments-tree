from datetime import datetime

from sqlalchemy import Boolean, Column, String, Integer, DateTime

from app.domain import User, Email
from app.infrastructure.database import Base


class UserDO(Base):
    """
    User DO
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
        return f"UserDO(id={self.id!r}, username={self.username!r})"

    def to_entity(self) -> User:
        """
        DO 转换成 Entity
        """
        return User(
            id=self.id,
            username=self.username,
            password=self.password,
            email=Email(self.email),
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(user: User) -> "UserDO":
        """
        Entity 转换成 DO
        """
        return UserDO(
            id=user.id,
            username=user.username,
            password=user.password,
            email=str(user.email),
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
