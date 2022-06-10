from typing import Optional

from pydantic import BaseModel, Field


class CommentCreateModel(BaseModel):
    """
    Comment Model 写模式(创建)
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
    parent_id: Optional[int] = Field(example=3)


class CommentUpdateModel(BaseModel):
    """
    Comment Model 写模式(更新)
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
