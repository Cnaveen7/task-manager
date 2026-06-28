from fastapi import FastAPI

from app.config.settings import settings
from app.routers.user_router import router as user_router


app = FastAPI(
    title=settings.app_name
)

app.include_router(user_router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }