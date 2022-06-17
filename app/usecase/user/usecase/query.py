from typing import List

from app.domain.user import UserDoesNotExistError
from app.domain.user.exception import AuthenticateError
from app.infrastructure.user import UserRepository
from app.utils import verify_password
from app.usecase.user.dto import UserReadDTO
from app.usecase.user.dto.query import UserLoginDTO


class UserQueryUseCase(object):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def fetch_one(self, user_id: int) -> UserReadDTO:
        try:
            user = self.repository.find(user_id)
            if not user:
                raise UserDoesNotExistError
        except:
            raise
        return UserReadDTO.from_entity(user)

    def authenticate(self, plain_password: str, username: str = None, email: str = None) -> UserLoginDTO:
        try:
            if username:
                user = self.repository.find_by_username(username)
            elif email:
                user = self.repository.find_by_email(email)
            else:
                user = None
            if not user:
                raise UserDoesNotExistError
        except:
            raise
        if not verify_password(plain_password=plain_password, encrypted_password=user.password):
            raise AuthenticateError
        return UserLoginDTO.from_entity(user)

    def fetch_all(self) -> List[UserReadDTO]:
        try:
            users = self.repository.find_all()
        except:
            raise
        return [UserReadDTO.from_entity(user) for user in users]
