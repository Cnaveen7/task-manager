from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dependencies.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
     
    username: Mapped[str] = mapped_column(String)

    email: Mapped[str] = mapped_column(String)

    hashed_password: Mapped[str] = mapped_column(String)

    todos: Mapped[list["Todo"]] = relationship(back_populates="user")