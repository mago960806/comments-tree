from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.comment import Comment


class CommentBaseRepository(ABC):
    """
    Comment Repository 接口
    """

    @abstractmethod
    def find(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError

    def find_all(self) -> List[Comment]:
        raise NotImplementedError

    @abstractmethod
    def save(self, comment: Comment) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, comment_id: int):
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError
