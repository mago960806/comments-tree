from typing import Optional

from app.domain.user import User, Email
from app.infrastructure.user import UserRepository
from app.usecase.user.dto import UserRegisterDTO, UserCreateDTO, UserReadDTO
from app.domain.user import UserIsAlreadyExistsError
from app.utils import encrypt_password


class UserCommandUseCase(object):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register_user(self, data: UserRegisterDTO) -> Optional[UserReadDTO]:
        user = User(
            username=data.username,
            password=encrypt_password(str(data.password)),
            email=Email(data.email),
            created_at=data.created_at,
        )
        if self.repository.exists(user):
            raise UserIsAlreadyExistsError
        created_user = self.repository.save(user)
        return UserReadDTO.from_entity(created_user)

    def create_user(self, data: UserCreateDTO) -> Optional[UserReadDTO]:
        user = User(
            username=data.username,
            password=encrypt_password(str(data.password)),
            email=Email(data.email),
            created_at=data.created_at,
            is_active=data.is_active,
            is_superuser=data.is_superuser,
        )
        if self.repository.exists(user):
            raise UserIsAlreadyExistsError
        created_user = self.repository.save(user)
        return UserReadDTO.from_entity(created_user)

    def delete_user(self, user_id: int):
        self.repository.remove(user_id)
