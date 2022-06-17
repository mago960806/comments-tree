from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentCreateDTO(BaseModel):
    """
    Comment Create Data Transfer Object
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
    parent_id: Optional[int] = Field(example=3)
    created_by: Optional[str] = "匿名用户"
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CommentUpdateDTO(BaseModel):
    """
    Comment Update Data Transfer Object
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
