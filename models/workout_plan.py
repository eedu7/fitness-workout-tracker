from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    to_start: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    to_end: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=True,
    )

    def __repr__(self):
        return f"WorkoutPlan: ID={self.id}, Name={self.name}, ToStart={self.to_start}"

    def __str__(self):
        return self.__repr__()
