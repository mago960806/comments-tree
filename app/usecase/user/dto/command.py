import re
import string

from pydantic import BaseModel, Field, validator, SecretStr as Password, EmailStr as Email


def check_username(username: str) -> str:
    username = username.lower()
    if not username.isalnum() or username.isnumeric():
        raise ValueError("用户名只能使用英文字母和数字组合, 不能包含汉字与特殊符号或者使用纯数字组合")
    return username


def check_password(password: str) -> str:
    # special_characters from https://owasp.org/www-community/password-special-characters
    special_characters = r" !\"  # $%&'()*+,-./:;<=>?@[\]^_`{|}~"
    allow_characters = string.ascii_letters + string.digits + special_characters
    # 密码内容校验: 校验密码中是否存在不允许的字符
    if not all([char in allow_characters for char in password]):
        raise ValueError("密码中只能包含大小写字母, 数字和特殊符号")
    # 密码复杂度校验: 至少包含一个大写、一个小写、一个数字、一个特殊符号
    if not re.search(r"\d", password):
        raise ValueError("密码中至少要包含一个数字")
    if not re.search(r"[a-z]", password):
        raise ValueError("密码中至少要包含一个小写字母")
    if not re.search(r"[A-Z]", password):
        raise ValueError("密码中至少要包含一个大写字母")
    if not re.search(r"[\u0020-\u0040\u005B-\u0060\u007B-\u007E]", password):
        raise ValueError("密码中至少要包含一个特殊符号")
    return password


class UserRegisterDTO(BaseModel):
    """
    User Register Data Transfer Object
    """

    username: str = Field(min_length=5, max_length=20, example="admin")
    password: Password = Field(min_length=8, max_length=20, example="Admin@123")
    email: Email

    _check_username = validator("username", allow_reuse=True)(check_username)

    @validator("password")
    def _check_password(cls, value: Password, **kwargs):
        password = value.get_secret_value()
        return check_password(password)


class UserCreateDTO(UserRegisterDTO):
    """
    User Create Data Transfer Object
    """

    is_active: bool = True
    is_superuser: bool = False
