from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship

from app.infrastructure.database import Base


class Comment(Base):
    """
    Comment DTO
    """

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    children = relationship("Comment")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"Comment(id={self.id!r}, parent_id={self.parent_id!r})"
