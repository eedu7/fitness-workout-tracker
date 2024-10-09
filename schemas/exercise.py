from pydantic import BaseModel, Field


class ExerciseCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the exercise.")
    description: str | None = Field(
        None, description="A detailed description of the exercise."
    )
    category_id: int = Field(
        ...,
        description="The category id of the exercise (e.g., Cardio, Strength).",
        examples=[1, 2],
    )
    muscle_group_id: int = Field(
        ...,
        description="The primary muscle group targeted by the exercise.",
        examples=[1, 2],
    )

    class Config:
        orm_mode = True


class ExerciseUpdate(ExerciseCreate):
    pass


class ExercisePartialUpdate(BaseModel):
    name: str | None = Field(
        None, description="The name of the exercise.", examples=["Cardio"]
    )
    description: str | None = Field(
        None, description="A detailed description of the exercise."
    )
    category_id: int | None = Field(
        None, description="The category id of the exercise.", examples=[1, 2]
    )
    muscle_group_id: int | None = Field(
        None, description="The primary muscle group id targeted by the exercise."
    )
