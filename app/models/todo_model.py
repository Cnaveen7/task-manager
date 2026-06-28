from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
  
from app.dependencies.database import Base

class Todo(Base):
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str]

    completed: Mapped[bool]

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="todos")