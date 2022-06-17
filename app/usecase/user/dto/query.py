from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.domain import User


class UserLoginDTO(BaseModel):
    """
    User Login Data Transfer Object
    """

    id: Optional[str] = None
    username: Optional[str] = None
    password: str
    email: Optional[str] = None

    @staticmethod
    def from_entity(user: User) -> "UserLoginDTO":
        return UserLoginDTO(
            id=user.id,
            username=user.username,
            password=user.password,
            email=user.email.value,
        )


class JWTTokenDTO(BaseModel):
    """
    JWT Token Data Transfer Object
    """

    token: str


class UserReadDTO(BaseModel):
    """
    User Read Data Transfer Object
    """

    id: Optional[int] = None
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_entity(user: User) -> "UserReadDTO":
        return UserReadDTO(
            id=user.id,
            username=user.username,
            email=user.email.value,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
