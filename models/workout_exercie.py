from sqlalchemy import Enum, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from schemas.workout import WorkoutStatus


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    workout_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workout_plans.id"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("exercises.id"), nullable=False
    )
    sets: Mapped[int] = mapped_column(Integer, nullable=True)
    repetitions: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    status: Mapped[WorkoutStatus] = mapped_column(
        Enum(WorkoutStatus), default=WorkoutStatus.TO_BE_STARTED
    )

    def __repr__(self):
        return f"<WorkoutExercise(id={self.id}, sets={self.sets}, repetitions={self.repetitions},weight={self.weight})>"

    def __str__(self):
        return self.__repr__()
