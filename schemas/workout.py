from enum import StrEnum

from pydantic import BaseModel, Field


class WorkoutStatus(StrEnum):
    COMPLETED = "completed"
    TO_BE_STARTED = "to_be_started"
    IN_PROGRESS = "in_progress"
    CANCELLED = "cancelled"


class WorkoutBase(BaseModel):
    workout_plan_id: int | None = Field(
        None, description="Workout plan ID", examples=[1]
    )
    sets: int | None = Field(None, description="Number of sets", examples=[1])
    repetitions: int | None = Field(
        None, description="Number of repetitions", examples=[1]
    )
    weight: float | None = Field(None, description="Workout weight", examples=[190])
    status: WorkoutStatus | None = Field(
        None, description="Workout status", examples=[WorkoutStatus.TO_BE_STARTED]
    )


class WorkoutCreate(WorkoutBase):
    description: str = Field(..., description="Description of the workout")
    exercise_id: int = Field(..., description="ID of the exercise", gt=0)


class WorkoutUpdate(WorkoutCreate):
    pass


class WorkoutPartialUpdate(WorkoutBase):
    description: str | None = Field(None, description="Description of the workout")
    exercise_id: int | None = Field(None, description="ID of the exercise", gt=0)
