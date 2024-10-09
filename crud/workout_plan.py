from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCrud
from models import WorkoutPlan


class WorkoutPlanCrud(BaseCrud[WorkoutPlan]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(WorkoutPlan, session)

    async def get_workout_plan_by_id(self, workout_plan_id: int) -> WorkoutPlan:
        try:
            workout: WorkoutPlan = await self.get_by_id(workout_plan_id)
            if not workout:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"WorkoutPlan with ID {workout_plan_id} not found",
                )
            return workout
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching workout plan: {str(e)}",
            )

    async def create_workout_plan(
            self, workout_plan_data: Dict[str, Any]
    ) -> WorkoutPlan:
        try:
            new_workout_plan = await self.create(
                workout_plan_data
            )  # Fixed recursive call issue
            return new_workout_plan
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating workout plan: {str(e)}",
            )

    async def update_workout_plan(
            self, workout_plan_id: int, workout_plan_data: Dict[str, Any]
    ) -> WorkoutPlan:
        try:
            updated_workout: WorkoutPlan = await self.update(
                workout_plan_id, workout_plan_data
            )
            if not updated_workout:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workout Plan with ID {workout_plan_id} not found",
                )
            return updated_workout
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating workout plan: {str(e)}",
            )

    async def delete_workout_plan(self, workout_plan_id: int) -> bool:
        try:
            deleted: bool = await self.delete(workout_plan_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"WorkoutPlan with ID {workout_plan_id} not found",
                )
            return deleted
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting workout plan: {str(e)}",
            )
