from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ExerciseCategory(str, Enum):
    CARDIO = "Cardio"
    STRENGTH = "Strength"
    FLEXIBILITY = "Flexibility"
    BALANCE = "Balance"
    OTHER = "Other"  # You can add more categories as needed


class MuscleGroup(str, Enum):
    CHEST = "Chest"
    BACK = "Back"
    LEGS = "Legs"
    ARMS = "Arms"
    SHOULDERS = "Shoulders"
    CORE = "Core"
    OTHER = "Other"  # You can add more muscle groups as needed


class ExerciseCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the exercise.")
    description: Optional[str] = Field(
        None, description="A detailed description of the exercise."
    )
    category: ExerciseCategory = Field(
        ...,
        description="The category of the exercise (e.g., Cardio, Strength).",
        examples=[
            ExerciseCategory.CARDIO,
            ExerciseCategory.STRENGTH,
            ExerciseCategory.FLEXIBILITY,
        ],
    )
    muscle_group: MuscleGroup = Field(
        ...,
        description="The primary muscle group targeted by the exercise.",
        examples=[MuscleGroup.CHEST, MuscleGroup.BACK, MuscleGroup.LEGS],
    )

    class Config:
        orm_mode = True  # This allows the model to work with SQLAlchemy objects
