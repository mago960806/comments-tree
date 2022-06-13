from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.domain.comment import Comment, CommentTreeNode


class CommentReadDTO(BaseModel):
    """
    Comment Read Data Transfer Object
    """

    id: int
    content: str
    parent_id: Optional[int] = None
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_entity(comment: Comment) -> "CommentReadDTO":
        return CommentReadDTO(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_by=comment.created_by,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


class CommentTreeNodeDTO(BaseModel):
    """
    Comment Tree Node Data Transfer Object
    """

    id: int
    content: str
    children: List["CommentTreeNodeDTO"] = []
    created_by: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_entity(comment: CommentTreeNode) -> "CommentTreeNodeDTO":
        comment_tree_dto = CommentTreeNodeDTO(
            id=comment.id,
            content=comment.content,
            created_by=comment.created_by,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
        children: List[CommentTreeNode] = comment.children
        if children:
            comment_tree_dto.children = [CommentTreeNodeDTO.from_entity(child) for child in children]
        return comment_tree_dto
