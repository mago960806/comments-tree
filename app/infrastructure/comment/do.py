from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList

from app.domain import Comment
from app.infrastructure.database import Base


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
        """
        DO 转换成 Entity
        """
        return get_comment_tree(self)

    @staticmethod
    def from_entity(comment: Comment) -> "CommentDO":
        """
        Entity 转换成 DO
        """
        return CommentDO(
            id=comment.id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


def get_comment_tree(comment_do: CommentDO) -> Comment:
    """
    递归获取单条评论下的子节点, 包括自身
    """
    comment_tree = Comment(
        id=comment_do.id,
        content=comment_do.content,
        created_at=comment_do.created_at,
        updated_at=comment_do.updated_at,
    )
    children: InstrumentedList = comment_do.children
    if children:
        comment_tree.children = [get_comment_tree(child) for child in children]
    return comment_tree
