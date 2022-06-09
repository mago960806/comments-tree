from abc import ABC, abstractmethod
from typing import Optional

from app.domain import Comment


class CommentBaseRepository(ABC):
    """
    Comment Repository 接口
    """

    @abstractmethod
    def find(self, comment: Comment) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def save(self, comment: Comment) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, comment_id: int):
        raise NotImplementedError
