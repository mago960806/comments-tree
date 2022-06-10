from typing import Optional, List

from app.domain.comment import CommentDoesNotExistError
from app.usecase.comment.models import CommentReadModel


class CommentQueryUseCase(object):
    def __init__(self, repository: "CommentRepository"):
        self.repository = repository

    def fetch_one(self, comment_id: int) -> Optional[CommentReadModel]:
        try:
            comment = self.repository.find(comment_id)
            if comment is None:
                raise CommentDoesNotExistError
        except:
            raise
        return comment

    def fetch_all(self) -> List[CommentReadModel]:
        try:
            comments = self.repository.find_all()
        except:
            raise
        return comments
