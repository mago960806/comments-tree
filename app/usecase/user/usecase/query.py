from typing import Optional, List

from app.domain.user import UserDoesNotExistError
from app.infrastructure.user import UserRepository
from app.usecase.user.dto import UserReadDTO


class UserQueryUseCase(object):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def fetch_one(self, user_id: int) -> Optional[UserReadDTO]:
        try:
            user = self.repository.find(user_id)
            if user is None:
                raise UserDoesNotExistError
        except:
            raise
        return UserReadDTO.from_entity(user)

    def fetch_all(self) -> List[UserReadDTO]:
        try:
            users = self.repository.find_all()
        except:
            raise
        return [UserReadDTO.from_entity(user) for user in users]
