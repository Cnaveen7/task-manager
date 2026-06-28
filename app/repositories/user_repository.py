from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate

def create_user(db: Session, user_create: UserCreate, hashed_password: str) -> User:
    user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_password
    )

    try:
        db.create(user)
        db.commit()
        db.refresh(user)

        return user
    except Exception:
        db.rollback()
        raise


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    statement = select(User).where(
        User.email == email
    )

    return db.scalar(statement)
