from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from loguru import logger
from sqlalchemy.orm.session import Session

from app.domain.comment import CommentDoesNotExistError
from app.infrastructure.comment import CommentRepository
from app.infrastructure.database import get_session
from app.usecase.comment import CommentCommandUseCase
from app.usecase.comment import CommentCreateDTO, CommentReadDTO
from app.usecase.comment.dto import CommentTreeNodeDTO
from app.usecase.comment.dto.query import CommentCountDTO
from app.usecase.comment.usecase import CommentQueryUseCase
from app.usecase.user import UserReadDTO
from .user import get_current_user, get_current_superuser

api = APIRouter()


def comment_command_usecase(session: Session = Depends(get_session)) -> CommentCommandUseCase:
    """
    创建 Comment Command UseCase 依赖
    """
    repository: CommentRepository = CommentRepository(session)
    return CommentCommandUseCase(repository)


def comment_query_usecase(session: Session = Depends(get_session)) -> CommentQueryUseCase:
    """
    创建 Comment Query UseCase 依赖
    """
    repository: CommentRepository = CommentRepository(session)
    return CommentQueryUseCase(repository)


@api.get("/comments", response_model=List[CommentTreeNodeDTO])
async def get_comments(
    query_usecase: CommentQueryUseCase = Depends(comment_query_usecase),
) -> List[CommentTreeNodeDTO]:
    """
    获取全部评论列表(未分页)
    权限要求: 无
    """
    comments = query_usecase.fetch_all()
    return comments
    # try:
    #     comments = query_usecase.fetch_all()
    # except Exception as e:
    #     logger.info(f"查询所有评论失败: {e}")
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"查询所有评论失败")
    # else:
    #     return comments


@api.get("/comments/{comment_id}", response_model=CommentReadDTO)
async def get_comment(
    comment_id: int,
    query_usecase: CommentQueryUseCase = Depends(comment_query_usecase),
) -> CommentReadDTO:
    """
    获取评论详情
    权限要求: 无
    """
    try:
        comment = query_usecase.fetch_one(comment_id)
    except CommentDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except Exception as e:
        logger.info(f"查询评论失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"查询评论失败")
    else:
        return comment


@api.post(
    "/comments",
    response_model=CommentReadDTO,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    data: CommentCreateDTO,
    command_usecase: CommentCommandUseCase = Depends(comment_command_usecase),
    current_user: UserReadDTO = Depends(get_current_user),
) -> CommentReadDTO:
    """
    创建评论
    权限要求: 已登录的用户
    """
    data.created_by = f"{current_user.username}({current_user.email})"
    try:
        comment = command_usecase.create_comment(data)
    except Exception as e:
        logger.info(f"创建评论失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="创建评论失败")
    else:
        return comment


@api.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    command_usecase: CommentCommandUseCase = Depends(comment_command_usecase),
    current_user: UserReadDTO = Depends(get_current_superuser),
):
    """
    创建评论
    权限要求: 已登录的超级用户
    """
    try:
        command_usecase.delete_comment(comment_id)
    except Exception as e:
        logger.info(f"删除评论失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="删除评论失败")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@api.get("/comments/count/", response_model=CommentCountDTO)
async def get_comment_count(
    query_usecase: CommentQueryUseCase = Depends(comment_query_usecase),
):
    """
    获取评论条数
    权限要求: 无
    """
    count = query_usecase.count()
    return {"count": count}
