from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCrud
from models import WorkoutExercise


class WorkoutCrud(BaseCrud[WorkoutExercise]):
    """
    CRUD operations for managing workouts in the database, specifically using the WorkoutExercise model.
    This class extends BaseCrud, providing methods for creating, reading, updating, and deleting workout data.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize the WorkoutCrud class with an async database session.

        Args:
            session (AsyncSession): The SQLAlchemy async session for database operations.
        """
        super().__init__(WorkoutExercise, session)


    async def get_workout_by_id(self, workout_id: int) -> WorkoutExercise:
        """
        Retrieve a workout by its ID from the database.

        Args:
            workout_id (int): The ID of the workout to retrieve.

        Returns:
            WorkoutExercise: The workout object if found.

        Raises:
            HTTPException: If the workout is not found or if an error occurs during the query.
        """
        try:
            workout: WorkoutExercise = await self.get_by_id(workout_id)
            if not workout:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workout with ID {workout_id} not found",
                )
            return workout
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error fetching workout: {str(e)}",
            )

    async def create_workout(self, workout_data: Dict[str, Any]) -> WorkoutExercise:
        """
        Create a new workout entry in the database.

        Args:
            workout_data (dict): A dictionary containing the workout data.

        Returns:
            WorkoutExercise: The newly created workout object.

        Raises:
            HTTPException: If an error occurs during the creation process.
        """
        try:
            new_workout = await self.create(**workout_data)  # Fixed recursive call issue
            return new_workout
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating workout: {str(e)}",
            )

    async def update_workout(self, workout_id: int, workout_data: Dict[str, Any]) -> WorkoutExercise:
        """
        Update an existing workout by its ID.

        Args:
            workout_id (int): The ID of the workout to update.
            workout_data (dict): A dictionary of updated workout data.

        Returns:
            WorkoutExercise: The updated workout object.

        Raises:
            HTTPException: If the workout is not found or if an error occurs during the update process.
        """
        try:
            updated_workout: WorkoutExercise = await self.update(workout_id, **workout_data)
            if not updated_workout:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workout with ID {workout_id} not found",
                )
            return updated_workout
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating workout: {str(e)}",
            )

    async def delete_workout(self, workout_id: int) -> bool:
        """
        Delete a workout by its ID from the database.

        Args:
            workout_id (int): The ID of the workout to delete.

        Returns:
            bool: True if the workout was successfully deleted, False otherwise.

        Raises:
            HTTPException: If the workout is not found or if an error occurs during the deletion process.
        """
        try:
            deleted: bool = await self.delete(workout_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Workout with ID {workout_id} not found",
                )
            return deleted
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting workout: {str(e)}",
            )
