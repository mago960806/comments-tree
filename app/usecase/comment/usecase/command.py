from typing import Optional

from app.domain.comment import Comment
from app.usecase.comment.dto import CommentCreateDTO, CommentReadDTO


class CommentCommandUseCase(object):
    def __init__(self, repository: "CommentRepository"):
        self.repository = repository

    def create_comment(self, data: CommentCreateDTO) -> Optional[CommentReadDTO]:
        comment = Comment(content=data.content, parent_id=data.parent_id)
        created_comment = self.repository.save(comment)
        return CommentReadDTO.from_entity(created_comment)

    def delete_comment(self, comment_id: int):
        self.repository.remove(comment_id)
