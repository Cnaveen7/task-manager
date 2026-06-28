from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate
from app.repositories.user_repository import (
    get_user_by_email,
    create_user
)
from app.core.security import hash_password

def register_user(
    db: Session,
    user_create: UserCreate
):

    existing_user = get_user_by_email(
        db,
        user_create.email
    )

    if existing_user:
        raise ValueError(
            "User with this email already exists"
        )

    hashed_password = hash_password(
        user_create.password
    )

    return create_user(
        db=db,
        user_create=user_create,
        hashed_password=hashed_password
    )