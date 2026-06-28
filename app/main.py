from fastapi import FastAPI

from app.config.settings import settings
from app.routers.user_router import router as user_router
from app.routers.auth_router import router as auth_router
from app.routers.todo_router import router as todo_router


app = FastAPI(
    title=settings.app_name
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(todo_router)


@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.app_name}"
    }