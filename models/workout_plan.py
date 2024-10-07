from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    data: Mapped[date] = mapped_column(Date, nullable=False, default=date.today())
    comments: Mapped[str] = mapped_column(Text, nullable=False)

    def __repr__(self):
        return f"<WorkoutPlan(id={self.id}, User_ID={self.user_id})>"

    def __str__(self):
        return self.__repr__()
