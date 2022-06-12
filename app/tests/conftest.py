import os

import pytest

from init_db import init_data
from .setup_test_db import TestingSessionLocal
from .setup_test_db import create_tables


@pytest.fixture(scope="session", autouse=True)
def cleanup(request: pytest.FixtureRequest):
    """
    测试数据库的创建与销毁
    """
    # 测试启动时自动执行
    create_tables()
    session = TestingSessionLocal()
    init_data(session)

    # 测试结束后自动执行
    def clean_db():
        os.unlink("test.db")

    request.addfinalizer(clean_db)
