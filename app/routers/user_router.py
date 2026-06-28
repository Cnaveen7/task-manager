from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.user_service import register_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/register",
    response_model=UserResponse
)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(
        db=db,
        user_create=user_create
    )
