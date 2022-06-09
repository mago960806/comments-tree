from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from app.domain.comment import Comment


class CommentReadModel(BaseModel):
    """
    Comment Model 读模式(查询)
    """

    id: int = Field(example=1)
    content: str = Field(example="测试评论")
    parent_id: Optional[int] = Field(example=3)
    created_at: Optional[datetime] = Field(example=datetime(year=2022, month=6, day=8))
    updated_at: Optional[datetime] = Field(example=datetime(year=2022, month=6, day=9))

    class Config:
        orm_mode = True

    @staticmethod
    def from_entity(comment: Comment) -> "CommentReadModel":
        return CommentReadModel(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
