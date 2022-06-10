from pydantic import BaseModel, EmailStr


class UserRegisterDTO(BaseModel):
    """
    User Register Data Transfer Object
    """

    username: str
    password: str
    email: EmailStr


class UserCreateDTO(UserRegisterDTO):
    """
    User Create Data Transfer Object
    """

    is_active: bool = True
    is_superuser: bool = False
