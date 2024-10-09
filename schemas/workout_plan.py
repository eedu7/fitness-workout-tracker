from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class WorkoutPlanCreate(BaseModel):
    name: str = Field(..., max_length=255, description="The name of the workout plan")
    description: Optional[str] = Field(None, description="The description of the workout plan")
    to_start: datetime = Field(default_factory=datetime.now, description="The start time of the workout plan")
    to_end: Optional[datetime] = Field(None, description="The end time of the workout plan")

    class Config:
        orm_mode = True

class WorkoutPlanUpdate(WorkoutPlanCreate):
    pass


class WorkoutPlanPartialUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255, description="The new name of the workout plan")
    description: Optional[str] = Field(None, description="The new description of the workout plan")
    to_start: Optional[datetime] = Field(None, description="The new start time of the workout plan")
    to_end: Optional[datetime] = Field(None, description="The new end time of the workout plan")

    class Config:
        orm_mode = True