from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workout_plan_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("workout_plans.id"), nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("exercises.id"), nullable=False
    )
    sets: Mapped[int] = mapped_column(Integer)
    repetitions: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)

    def __repr__(self):
        return f"<WorkoutExercise(id={self.id}, sets={self.sets}, repetitions={self.repetitions},weight={self.weight})>"

    def __str__(self):
        return self.__repr__()
