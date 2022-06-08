from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.databases import BaseModel


class Comment(BaseModel):
    """
    留言模型
    """

    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    children = relationship("Comment")

    def __repr__(self):
        return f"Comment(id={self.id!r}, parent_id={self.parent_id!r})"
