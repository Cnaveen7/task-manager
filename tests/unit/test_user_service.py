import pytest
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate
from app.services.user_service import register_user
from app.models.user_model import User

def test_register_user_success(db_session: Session):
    user_in = UserCreate(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    
    # Register the user
    user = register_user(db_session, user_in)
    
    assert user.id is not None
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    # The password must be hashed and stored, not plain text
    assert user.hashed_password != "testpassword"

def test_register_user_duplicate_email(db_session: Session):
    user_in1 = UserCreate(
        username="user1",
        email="duplicate@example.com",
        password="password1"
    )
    user_in2 = UserCreate(
        username="user2",
        email="duplicate@example.com",
        password="password2"
    )
    
    # First registration should succeed
    register_user(db_session, user_in1)
    
    # Second registration with duplicate email should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        register_user(db_session, user_in2)
        
    assert str(exc_info.value) == "User with this email already exists"
