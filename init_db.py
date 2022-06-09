from app.infrastructure.database import create_tables


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
