from typing import Optional

from pydantic import BaseModel, Field


class CommentCreateDTO(BaseModel):
    """
    Comment Create Data Transfer Object
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
    parent_id: Optional[int] = Field(example=3)


class CommentUpdateDTO(BaseModel):
    """
    Comment Update Data Transfer Object
    """

    content: str = Field(min_length=3, max_length=200, example="测试评论")
