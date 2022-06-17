from sqlalchemy.orm import Session

from app.infrastructure import UserRepository
from app.infrastructure.database import SessionLocal
from app.infrastructure.database import create_tables
from app.usecase.user import UserCreateDTO, UserCommandUseCase


def init_data(session: Session) -> None:
    """
    初始化数据
    """
    repository = UserRepository(session)
    command_usecase = UserCommandUseCase(repository)

    normal_user = UserCreateDTO(username="test1", password="Test1@123", email="test1@devops.com")
    superuser = UserCreateDTO(username="admin", password="Admin@123", email="admin@devops.com", is_superuser=True)
    command_usecase.create_user(normal_user)
    command_usecase.create_user(superuser)


if __name__ == "__main__":
    print("数据初始化...")
    create_tables()
    session = SessionLocal()
    init_data(session)
    print("数据初始化完毕.")
