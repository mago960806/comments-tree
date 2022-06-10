from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from loguru import logger
from sqlalchemy.orm.session import Session

from app.domain.user import UserDoesNotExistError, UserIsAlreadyExistsError
from app.infrastructure.database import get_session
from app.infrastructure.user import UserRepository
from app.usecase.user import UserQueryUseCase, UserCommandUseCase
from app.usecase.user import UserRegisterDTO, UserCreateDTO, UserReadDTO

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


@api.post("/register")
async def register_user(
    data: UserRegisterDTO,
    command_usecase: UserCommandUseCase = Depends(user_command_usecase),
):
    try:
        user = command_usecase.register_user(data)
    except UserIsAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)
    except Exception as e:
        logger.info(f"注册用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="注册用户失败")
    else:
        return user


@api.get("/users", response_model=List[UserReadDTO])
async def get_users(
    query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
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
):
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
):
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
):
    try:
        command_usecase.delete_user(user_id)
    except Exception as e:
        logger.info(f"删除用户失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="删除用户失败")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
