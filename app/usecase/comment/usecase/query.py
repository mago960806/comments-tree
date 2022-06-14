from typing import Optional, List

from app.domain.comment import CommentDoesNotExistError
from app.usecase.comment.dto import CommentReadDTO, CommentTreeNodeDTO


class CommentQueryUseCase(object):
    def __init__(self, repository: "CommentRepository"):
        self.repository = repository

    def fetch_one(self, comment_id: int) -> Optional[CommentReadDTO]:
        try:
            comment = self.repository.find(comment_id)
            if comment is None:
                raise CommentDoesNotExistError
        except:
            raise
        return CommentReadDTO.from_entity(comment)

    def fetch_all(self) -> List[CommentTreeNodeDTO]:
        try:
            comments = self.repository.find_all()
        except:
            raise
        return [CommentTreeNodeDTO.from_entity(comment) for comment in comments]

    def count(self) -> int:
        return self.repository.count()
