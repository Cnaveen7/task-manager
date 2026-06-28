from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user_model import User
from app.schemas.todo_schema import CreateTodo, TodoResponse, UpdateTodo
from app.services.todo_service import (
    create_user_todo,
    get_user_todos,
    get_user_todo,
    update_user_todo,
    delete_user_todo
)

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create(
    todo_create: CreateTodo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_user_todo(db, todo_create, current_user.id)

@router.get("", response_model=List[TodoResponse])
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_todos(db, current_user.id)

@router.get("/{todo_id}", response_model=TodoResponse)
def get(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_user_todo(db, todo_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.put("/{todo_id}", response_model=TodoResponse)
def update(
    todo_id: int,
    todo_update: UpdateTodo,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_user_todo(db, todo_id, todo_update, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        delete_user_todo(db, todo_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
