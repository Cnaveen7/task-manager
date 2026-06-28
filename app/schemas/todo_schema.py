from typing import Optional
from pydantic import BaseModel, ConfigDict


class CreateTodo(BaseModel):
    title: str
    completed: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class UpdateTodo(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None