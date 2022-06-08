from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.databases import BaseModel


class Comment(BaseModel):
    """
    留言模型
    """

    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    children = relationship("Comment")
