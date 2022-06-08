from app.databases import engine, BaseModel
from app.models import User, Comment


def create_tables() -> None:
    """
    创建数据表
    """
    BaseModel.metadata.create_all(engine)


def init_data() -> None:
    """
    初始化数据
    """
    pass


if __name__ == "__main__":
    print("数据初始化...")
    create_tables()
    init_data()
    print("数据初始化完毕.")
