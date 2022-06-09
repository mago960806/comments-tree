from abc import ABC, abstractmethod
from typing import Optional

from app.domain.comment import Comment


class CommentBaseRepository(ABC):
    """
    Comment Repository 抽象基类
    """

    @abstractmethod
    def create(self, comment: Comment) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def update(self, comment: Comment) -> Optional[Comment]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, comment_id: int):
        raise NotImplementedError
