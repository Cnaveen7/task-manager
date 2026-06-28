from typing import Optional, Sequence
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo_model import Todo
from app.schemas.todo_schema import CreateTodo, UpdateTodo

def create_todo(db: Session, todo_create: CreateTodo, user_id: int) -> Todo:
    todo = Todo(
        title=todo_create.title,
        completed=todo_create.completed,
        user_id=user_id
    )
    try:
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo
    except Exception:
        db.rollback()
        raise

def get_todos_by_user(db: Session, user_id: int) -> Sequence[Todo]:
    statement = select(Todo).where(Todo.user_id == user_id)
    return db.scalars(statement).all()

def get_todo_by_id(db: Session, todo_id: int) -> Optional[Todo]:
    statement = select(Todo).where(Todo.id == todo_id)
    return db.scalar(statement)

def update_todo(db: Session, db_todo: Todo, todo_update: UpdateTodo) -> Todo:
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_todo, key, value)
    try:
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    except Exception:
        db.rollback()
        raise

def delete_todo(db: Session, db_todo: Todo) -> None:
    try:
        db.delete(db_todo)
        db.commit()
    except Exception:
        db.rollback()
        raise
