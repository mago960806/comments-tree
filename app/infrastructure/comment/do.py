from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList

from app.domain.comment import Comment, CommentTreeNode
from app.infrastructure.database import Base


class CommentDO(Base):
    """
    Comment Data Object
    """

    __tablename__ = "comment"

    id = Column(Integer, primary_key=True)
    content = Column(Text(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("comment.id"), nullable=True)
    children = relationship("CommentDO")
    created_by = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"CommentDO(id={self.id!r}, content={self.content!r}, parent_id={self.parent_id!r})"

    def to_entity(self) -> Comment:
        """
        DO 转换成 Entity
        """
        return Comment(
            id=self.id,
            content=self.content,
            parent_id=self.parent_id,
            created_by=self.created_by,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(comment: Comment) -> "CommentDO":
        """
        Entity 转换成 DO
        """
        return CommentDO(
            id=comment.id,
            content=comment.content,
            parent_id=comment.parent_id,
            created_by=comment.created_by,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
        )


def get_comments_tree(comment_dos: List[CommentDO]) -> List[CommentTreeNode]:
    """
    获取整个评论树及其子节点
    :param comment_dos: parent_id 为 None 的 CommentDo 列表
    :return: List[CommentTreeNode]
    """
    return [get_comment_tree(comment_do) for comment_do in comment_dos]


def get_comment_tree(comment_do: CommentDO) -> CommentTreeNode:
    """
    递归获取单条评论下的子节点, 包括自身
    """
    comment_tree = CommentTreeNode(
        id=comment_do.id,
        content=comment_do.content,
        created_by=comment_do.created_by,
        created_at=comment_do.created_at,
        updated_at=comment_do.updated_at,
    )
    children: InstrumentedList = comment_do.children
    if children:
        comment_tree.children = [get_comment_tree(child) for child in children]
    return comment_tree
