import uvicorn

from app.config import settings


from fastapi import FastAPI
from app.routers import user_api, comment_api

app = FastAPI()

app.include_router(user_api, prefix="/api/v1")
app.include_router(comment_api, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
