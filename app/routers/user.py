from typing import List, Dict

from fastapi import APIRouter, status, Depends, HTTPException, Response
from jose import jwt
from loguru import logger
from sqlalchemy.orm.session import Session

from app.config import settings
from app.domain import User
from app.domain.user import UserDoesNotExistError, UserIsAlreadyExistsError
from app.domain.user.exception import AuthenticateError
from app.infrastructure.database import get_session
from app.infrastructure.user import UserRepository
from app.usecase.user import UserQueryUseCase, UserCommandUseCase
from app.usecase.user import UserRegisterDTO, UserCreateDTO, UserReadDTO
from app.usecase.user.dto.query import JWTTokenDTO, UserLoginDTO
from app.utils import get_authorization_from_headers, create_access_token

api = APIRouter()


def user_command_usecase(session: Session = Depends(get_session)) -> UserCommandUseCase:
    """
    创建 User Command UseCase 依赖
    """
    repository: UserRepository = UserRepository(session)
    return UserCommandUseCase(repository)


def user_query_usecase(session: Session = Depends(get_session)) -> UserQueryUseCase:
    """
    创建 User Query UseCase 依赖
    """
    repository: UserRepository = UserRepository(session)
    return UserQueryUseCase(repository)


def get_current_user(
    token: str = Depends(get_authorization_from_headers),
    query_usecase: UserQueryUseCase = Depends(user_query_usecase),
) -> UserReadDTO:
    """
    通过 JWT 获取当前登录的用户
    :param token: 通过请求头的 Authorization 字段获取 JWT
    :param query_usecase: 查询案例
    """
    try:
        payload: Dict[str, str] = jwt.decode(token, settings.SECRET_KEY)
    except jwt.JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token已失效")
    try:
        user = query_usecase.fetch_one(user_id=int(payload.get("sub")))
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="用户未激活")
    return user


def get_current_superuser(
    current_user: UserReadDTO = Depends(get_current_user),
) -> UserReadDTO:
    """
    通过 JWT 获取当前登录的超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="当前用户权限不足")
    return current_user


@api.post("/login", response_model=JWTTokenDTO)
async def login(data: UserLoginDTO, query_usecase: UserQueryUseCase = Depends(user_query_usecase)):
    """
    用户登录
    权限要求: 无
    """
    try:
        user = query_usecase.authenticate(username=data.username, email=data.email, plain_password=data.password)
    except (UserDoesNotExistError, AuthenticateError) as e:
        # 避免用户名爆破攻击, 不能直接返回真实原因
        logger.info(f"用户登录失败: 用户名={data.username}, 原因={e.message}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名或密码不正确")
    except Exception as e:
        logger.error(f"系统错误: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="系统错误")
    else:
        access_token = create_access_token(subject=str(user.id))
        return {"token": access_token}


@api.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserReadDTO)
async def register(
    data: UserRegisterDTO,
    command_usecase: UserCommandUseCase = Depends(user_command_usecase),
) -> UserReadDTO:
    """
    用户注册
    权限要求: 无
    """
    try:
        user = command_usecase.register_user(data)
    except UserIsAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.info(f"注册用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="注册用户失败")
    else:
        return user


@api.get("/users/me", response_model=UserReadDTO)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前登录用户信息
    权限要求: 已登录的用户
    """
    return current_user


@api.get("/users", response_model=List[UserReadDTO])
async def get_users(
    query_usecase: UserQueryUseCase = Depends(user_query_usecase),
    current_user: UserReadDTO = Depends(get_current_superuser),
) -> List[UserReadDTO]:
    """
    获取全部用户列表(未分页)
    权限要求: 已登录的超级用户
    """
    try:
        users = query_usecase.fetch_all()
    except Exception as e:
        logger.info(f"查询所有用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="查询所有用户失败")
    else:
        return users


@api.get("/users/{user_id}", response_model=UserReadDTO)
async def get_user(
    user_id: int,
    query_usecase: UserQueryUseCase = Depends(user_query_usecase),
    current_user: UserReadDTO = Depends(get_current_superuser),
):
    """
    获取用户详情
    权限要求: 已登录的超级用户
    """
    try:
        user = query_usecase.fetch_one(user_id)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        logger.info(f"查询用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"查询用户失败: {e}")
    else:
        return user


@api.post(
    "/users",
    response_model=UserReadDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserCreateDTO,
    command_usecase: UserCommandUseCase = Depends(user_command_usecase),
    current_user: UserReadDTO = Depends(get_current_superuser),
):
    """
    创建用户
    权限要求: 已登录的超级用户
    """
    try:
        user = command_usecase.create_user(data)
    except UserIsAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.info(f"创建用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="创建用户失败")
    else:
        return user


@api.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    command_usecase: UserCommandUseCase = Depends(user_command_usecase),
    current_user: UserReadDTO = Depends(get_current_superuser),
):
    """
    删除指定用户
    权限要求: 已登录的超级用户
    """
    try:
        command_usecase.delete_user(user_id)
    except Exception as e:
        logger.info(f"删除用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="删除用户失败")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
