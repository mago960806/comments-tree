from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList

from app.domain import Comment
from app.infrastructure.database import Base
from app.usecase.comment import CommentReadModel


class CommentDO(Base):
    """
    Comment Data Object
    """

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"))
    children = relationship("CommentDO")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow())
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"CommentDO(id={self.id!r}, content={self.content!r}, parent_id={self.parent_id!r})"

    def to_entity(self) -> Comment:
        return Comment(
            id=self.id,
            content=self.content,
            parent_id=self.parent_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def to_read_model(self) -> CommentReadModel:
        return get_comment_tree(self)

    @staticmethod
    def from_entity(comment: Comment) -> "CommentDO":
        return CommentDO(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


def get_comment_tree(comment_do: CommentDO) -> CommentReadModel:
    """
    递归获取单条评论下的子节点, 包括自身
    """

    comment_tree = CommentReadModel(
        id=comment_do.id,
        content=comment_do.content,
        created_at=comment_do.created_at,
        updated_at=comment_do.updated_at,
    )
    children: InstrumentedList = comment_do.children
    if children:
        comment_tree.children = [get_comment_tree(child) for child in children]
    return comment_tree
