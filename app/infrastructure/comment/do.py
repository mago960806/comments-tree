from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.comment import Comment
from app.infrastructure.database import Base
from app.usecase.comment import CommentReadModel


class CommentDTO(Base):
    """
    Comment DTO
    """

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    children = relationship("CommentDTO")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"CommentDTO(id={self.id!r}, content={self.content!r}, parent_id={self.parent_id!r})"

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            content=self.content,
            parent_id=self.parent_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> CommentReadModel:
        return CommentReadModel(
            id=self.id,
            content=self.content,
            parent_id=self.parent_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(comment: Comment) -> "CommentDTO":
        return CommentDTO(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )
