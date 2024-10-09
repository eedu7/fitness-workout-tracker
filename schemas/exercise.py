from typing import Optional

from pydantic import BaseModel, Field


class ExerciseCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the exercise.")
    description: Optional[str] = Field(
        None, description="A detailed description of the exercise."
    )
    category_id: int = Field(
        ...,
        description="The category id of the exercise (e.g., Cardio, Strength).",
        examples=[1, 2
                  ],
    )
    muscle_group_id: int = Field(
        ...,
        description="The primary muscle group targeted by the exercise.",
        examples=[1, 2],
    )

    class Config:
        orm_mode = True

