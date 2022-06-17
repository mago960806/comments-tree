import pytest

from app.usecase.user.dto.command import check_username, check_password, UserRegisterDTO


def test_check_username():
    assert check_username("admin")
    with pytest.raises(ValueError):
        check_username("admin@devops")  # 出现特殊符号
        check_username("管理员")  # 出现汉字
        check_username("123")  # 纯数字组合


def test_check_password():
    assert check_password("Admin@123")
    with pytest.raises(ValueError):
        check_password("密码")  # 出现不允许的字符
        check_password("Admin@")  # 没有数字
        check_password("123456@")  # 没有小写字母
        check_password("admin@123456")  # 没有大写字母
        check_password("Admin123456")  # 没有特殊符号


def test_user_register_dto():
    UserRegisterDTO(username="admin", password="Admin@123", email="admin@devops.com")

    with pytest.raises(ValueError):
        UserRegisterDTO(username="aaa", password="Admin@123", email="admin@devops.com")  # 用户名过短
        UserRegisterDTO(username="aaa" * 10, password="Admin@123", email="admin@devops.com")  # 用户名过长
        UserRegisterDTO(username="admin", password="A@1", email="admin@devops.com")  # 密码过短
        UserRegisterDTO(username="admin", password="Admin@123" * 10, email="admin@devops.com")  # 密码过长
        UserRegisterDTO(username="admin", password="Admin@123", email="admin!devops.com")  # 邮箱格式不正确
