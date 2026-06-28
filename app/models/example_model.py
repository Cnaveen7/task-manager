from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Enum as SQLEnum, JSON, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.dependencies.database import Base


class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class ExampleModel(Base):
    __tablename__ = "examples"

    # int
    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    # str
    name: Mapped[str]

    # bool
    is_verified: Mapped[bool] = mapped_column(
        default=False
    )

    # datetime
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # date
    birth_date: Mapped[date] = mapped_column(
        Date
    )

    # Decimal
    salary: Mapped[Decimal] = mapped_column(
        Numeric(10, 2)
    )

    # JSON
    preferences: Mapped[dict] = mapped_column(
        JSON
    )

    # Enum
    status: Mapped[Status] = mapped_column(
        SQLEnum(Status)
    )

    # UUID
    public_id: Mapped[UUID] = mapped_column(
        default=uuid4,
        unique=True
    )

    # Long text
    description: Mapped[str] = mapped_column(
        Text
    )