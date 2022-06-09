from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.comment import CommentBaseRepository, Comment
from app.infrastructure.comment.dto import CommentDTO


class CommentRepository(CommentBaseRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, comment: Comment):
        comment_dto = CommentDTO.from_entity(comment)
        try:
            self.session.add(comment_dto)
        except:
            self.session.rollback()
            raise
        else:
            self.session.commit()
            return comment_dto.to_entity()

    def find_by_id(self, comment_id: int) -> Optional[Comment]:
        try:
            comment_dto: CommentDTO = self.session.query(CommentDTO).filter_by(id=comment_id).one()
        except NoResultFound:
            return None
        else:
            return comment_dto.to_entity()

    def update(self, comment: Comment):
        raise NotImplementedError

    def delete_by_id(self, comment_id: int):
        raise NotImplementedError
