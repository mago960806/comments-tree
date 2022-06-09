from abc import ABC, abstractmethod
from typing import Optional

from app.domain.user import User


class UserBaseRepository(ABC):
    """
    User Repository 抽象基类
    """

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, user_id: int):
        raise NotImplementedError
