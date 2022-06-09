from typing import Optional

from app.domain.comment import Comment
from app.usecase.comment.models import CommentCreateModel, CommentReadModel


class CommentCommandUseCase(object):
    def __init__(self, repository: "CommentRepository"):
        self.repository = repository

    def create_comment(self, data: CommentCreateModel) -> Optional[CommentReadModel]:
        comment = Comment(content=data.content, parent_id=data.parent_id)
        created_comment = self.repository.create(comment)
        return CommentReadModel.from_entity(created_comment)
