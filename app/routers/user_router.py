from fastapi import APIRouter, Depends, HTTPException, status
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
    try:
        return register_user(
            db=db,
            user_create=user_create
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

