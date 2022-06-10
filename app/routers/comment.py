from fastapi import APIRouter, status, Depends, HTTPException, Response
from loguru import logger
from sqlalchemy.orm.session import Session

from app.infrastructure.comment import CommentRepository
from app.infrastructure.database import get_session
from app.usecase.comment import CommentCommandUseCase
from app.usecase.comment import CommentCreateModel, CommentReadModel


api = APIRouter()


def comment_command_usecase(session: Session = Depends(get_session)) -> CommentCommandUseCase:
    """
    创建 CommentCommandUseCase 依赖
    """
    repository: CommentRepository = CommentRepository(session)
    return CommentCommandUseCase(repository)


@api.post(
    "/comments",
    response_model=CommentReadModel,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    data: CommentCreateModel,
    command_usecase: CommentCommandUseCase = Depends(comment_command_usecase),
):
    try:
        comment = command_usecase.create_comment(data)
    except Exception as e:
        logger.info(f"创建评论失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="评论失败")
    else:
        return comment


@api.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    command_usecase: CommentCommandUseCase = Depends(comment_command_usecase),
):
    try:
        command_usecase.delete_comment(comment_id)
    except Exception as e:
        logger.info(f"删除评论失败: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="评论不存在")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
