from abc import ABC, abstractmethod
from typing import Optional

from app.domain.user import User


class UserBaseRepository(ABC):
    """
    User Repository 接口
    """

    @abstractmethod
    def find(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, user_id: int):
        raise NotImplementedError
