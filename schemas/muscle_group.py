from pydantic import BaseModel, Field
class MuscleGroupCreate(BaseModel):
    name: str = Field(..., examples=["Chest"])
    description: str = Field(..., examples=["Exercises that target the pectoral muscles, including bench presses, push-ups, and chest flies."])

class MuscleGroupUpdate(MuscleGroupCreate):
    pass

class MuscleGroupPartialUpdate(BaseModel):
    name: str | None = Field(None, examples=["Chest"])
    description: str | None = Field(None, examples=[
        "Exercises that target the pectoral muscles, including bench presses, push-ups, and chest flies."])
