import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.config import settings
from app.routers import user, comment

app = FastAPI(title="Comments Tree", description="A Domain-Drive Design project in FastAPI")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    统一异常捕获
    """
    error_message = exc.errors()[0].get("msg")
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"detail": error_message})


app.include_router(user.api, prefix="/api/v1", tags=["users"])
app.include_router(comment.api, prefix="/api/v1", tags=["comments"])


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
