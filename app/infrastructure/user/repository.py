from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session
from sqlalchemy.sql import exists
from app.domain.user import User, UserBaseRepository
from app.infrastructure.user.do import UserDO
from sqlalchemy import or_


class UserRepository(UserBaseRepository):
    """
    User Repository 实现
    """

    def __init__(self, session: Session):
        self.session: Session = session

    def find(self, user_id: int) -> Optional[User]:
        try:
            user_do: UserDO = self.session.query(UserDO).filter_by(id=user_id).one()
        except NoResultFound:
            return None
        else:
            return user_do.to_entity()

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            user_do: UserDO = self.session.query(UserDO).filter_by(email=email).one()
        except NoResultFound:
            return None
        else:
            return user_do.to_entity()

    def exists(self, user: User) -> bool:
        is_user_exists = self.session.query(
            self.session.query(UserDO)
            .filter(or_(UserDO.username == user.username, UserDO.email == user.email.value))
            .exists()
        ).scalar()
        return is_user_exists

    def find_all(self) -> List[User]:
        user_dos: List[UserDO] = self.session.query(UserDO).order_by(UserDO.created_at).all()
        return [user_do.to_entity() for user_do in user_dos]

    def save(self, user: User) -> Optional[User]:
        if not user.id:
            # Create
            user_do = UserDO.from_entity(user)
            try:
                self.session.add(user_do)
            except:
                self.session.rollback()
                raise
            else:
                self.session.commit()
                return user_do.to_entity()
        else:
            # Update
            pass

    def remove(self, user_id: int):
        try:
            user_do: UserDO = self.session.query(UserDO).filter_by(id=user_id).one()
        except NoResultFound:
            return None
        else:
            self.session.delete(user_do)
            self.session.commit()
