from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.comment import CommentBaseRepository, Comment
from app.infrastructure.comment.do import CommentDO


class CommentRepository(CommentBaseRepository):
    """
    Comment Repository 实现
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find(self, comment_id: int) -> Optional[Comment]:
        try:
            comment_do: CommentDO = self.session.query(CommentDO).filter_by(id=comment_id).one()
        except NoResultFound:
            return None
        else:
            return comment_do.to_entity()

    def save(self, comment: Comment) -> Optional[Comment]:
        if not comment.id:
            # Create
            comment_do = CommentDO.from_entity(comment)
            try:
                self.session.add(comment_do)
            except:
                self.session.rollback()
                raise
            else:
                self.session.commit()
                return comment_do.to_entity()
        else:
            # Update
            pass

    def remove(self, comment_id: int):
        try:
            comment_do: CommentDO = self.session.query(CommentDO).filter_by(id=comment_id).one()
        except NoResultFound:
            return None
        else:
            self.session.delete(comment_do)
            self.session.commit()
