from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional, List

from app.domain.comment import Comment


class CommentReadDTO(BaseModel):
    """
    Comment Read Data Transfer Object
    """

    id: int = Field(example=1)
    content: str = Field(example="测试评论")
    children: List["CommentReadDTO"] = Field(default=[])
    created_at: Optional[datetime] = Field(example=datetime(year=2022, month=6, day=8))
    updated_at: Optional[datetime] = Field(example=datetime(year=2022, month=6, day=9))

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(comment: Comment) -> "CommentReadDTO":
        return CommentReadDTO(
            id=comment.id,
            content=comment.content,
            children=comment.children,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
