from pydantic import BaseModel, Field


class CategoryCreateData(BaseModel):
    name: str = Field(..., examples=["Endurance"])
    description: str = Field(
        ...,
        examples=[
            "Training designed to increase stamina and overall fitness, typically involving prolonged activities."
        ],
    )


class CategoryUpdateData(CategoryCreateData):
    pass


class CategoryPartialUpdateData(BaseModel):
    name: str | None = Field(None, examples=["Endurance"])
    description: str | None = Field(
        None,
        examples=[
            "Training designed to increase stamina and overall fitness, typically involving prolonged activities."
        ],
    )
