import uvicorn

from app.config import settings


from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def home():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
