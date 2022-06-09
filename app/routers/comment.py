from fastapi import APIRouter, status, Depends, HTTPException
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
        logger.info(f"评论失败: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="评论失败")
    else:
        return comment
