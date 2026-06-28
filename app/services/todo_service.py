from typing import Sequence
from sqlalchemy.orm import Session

from app.models.todo_model import Todo
from app.schemas.todo_schema import CreateTodo, UpdateTodo
from app.repositories.todo_repository import (
    create_todo,
    get_todos_by_user,
    get_todo_by_id,
    update_todo,
    delete_todo
)

def get_user_todos(db: Session, user_id: int) -> Sequence[Todo]:
    return get_todos_by_user(db, user_id)

def get_user_todo(db: Session, todo_id: int, user_id: int) -> Todo:
    todo = get_todo_by_id(db, todo_id)
    if not todo:
        raise ValueError("Todo not found")
    if todo.user_id != user_id:
        raise PermissionError("Not authorized to access this todo")
    return todo

def create_user_todo(db: Session, todo_create: CreateTodo, user_id: int) -> Todo:
    return create_todo(db, todo_create, user_id)

def update_user_todo(db: Session, todo_id: int, todo_update: UpdateTodo, user_id: int) -> Todo:
    # Verifies ownership before updating
    todo = get_user_todo(db, todo_id, user_id)
    return update_todo(db, todo, todo_update)

def delete_user_todo(db: Session, todo_id: int, user_id: int) -> None:
    # Verifies ownership before deleting
    todo = get_user_todo(db, todo_id, user_id)
    delete_todo(db, todo)
