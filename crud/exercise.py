from typing import List

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCrud
from models import Exercise


class ExerciseCrud(BaseCrud[Exercise]):
    """
    CRUD operations for Exercise model.

    This class provides methods to perform create, read, update, and delete
    operations on Exercise instances.

    Attributes:
        session (AsyncSession): An asynchronous SQLAlchemy session for database operations.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the ExerciseCrud with a SQLAlchemy session.

        Args:
            session (AsyncSession): The SQLAlchemy session for performing database operations.
        """
        super().__init__(model=Exercise, session=session)

    async def get_all_exercise(self, skip: int = 0, limit: int = 100) -> List[Exercise]:
        """
        Retrieves all Exercise instances, with optional pagination.

        Args:
            skip (int): The number of items to skip (default is 0).
            limit (int): The maximum number of items to return (default is 100).

        Raises:
            HTTPException: If no exercises are found or on other errors.

        Returns:
            List[Exercise]: A list of Exercise instances.
        """
        try:
            exercise = await self.get_all(skip=skip, limit=limit)
            if not exercise:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No exercises found",
                )
            return exercise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error on fetching all exercise: {e}",
            )

    async def get_by_id(self, exercise_id: int) -> Exercise:
        """
        Retrieves an Exercise instance by its ID.

        Args:
            exercise_id (int): The ID of the Exercise instance to retrieve.

        Raises:
            HTTPException: If the exercise with the given ID is not found or on other errors.

        Returns:
            Exercise: The Exercise instance with the specified ID.
        """
        try:
            exercise = await self.get_by(field="id", value=exercise_id)

            if not exercise:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Exercise with id: {exercise_id} not found",
                )
            return exercise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error on fetching exercie with id: {exercise_id}: {str(e)}",
            )

    async def get_by_name(self, name: str) -> Exercise:
        """
        Retrieves an Exercise instance by its name.

        Args:
            name (str): The name of the Exercise instance to retrieve.

        Raises:
            HTTPException: If the exercise with the given name is not found or on other errors.

        Returns:
            Exercise: The Exercise instance with the specified name.
        """

        try:
            exercise = await self.get_by(field="name", value=name)
            if not exercise:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Exercise with name {name} not found",
                )
            return exercise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error on fetching exercise with name: {name}: {str(e)}",
            )

    async def create_exercise(self, name: str, description: str) -> Exercise:
        """
        Creates a new Exercise instance.

        Args:
            name (str): The name of the exercise.
            description (str): A description of the exercise.

        Raises:
            HTTPException: If an exercise with the same name already exists or on other errors.

        Returns:
            Exercise: The newly created Exercise instance.
        """
        try:
            exercise = await self.get_by_name(name=name)
            if exercise:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Exercise with name {name} already exists",
                )
            new_exercise = await self.create(
                {
                    "name": name,
                    "description": description,
                }
            )
            return new_exercise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error on creating exercise with name: {name}: {str(e)}",
            )

    async def update_exercise(
        self, exercise_id: int, name: str | None = None, description: str | None = None
    ) -> Exercise:
        """
        Updates an existing Exercise instance.

        Args:
            exercise_id (int): The ID of the exercise to update.
            name (str | None): The new name of the exercise (if provided).
            description (str | None): The new description of the exercise (if provided).

        Raises:
            HTTPException: If the exercise with the given ID is not found or on other errors.

        Returns:
            Exercise: The updated Exercise instance.
        """
        try:
            data = {}
            if name:
                data["name"] = name
            if description:
                data["description"] = description

            await self.get_by_id(exercise_id)  # Checking if exercise exists

            updated_exercise = await self.update(exercise_id, **data)
            return updated_exercise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error on updating exercise with name: {name}: {str(e)}",
            )

    async def delete_exercise(self, exercise_id: int) -> JSONResponse:
        """
        Deletes an Exercise instance by its ID.

        Args:
            exercise_id (int): The ID of the Exercise instance to delete.

        Raises:
            HTTPException: If the exercise with the given ID is not found or on other errors.

        Returns:
            JSONResponse: A response indicating the deletion of the exercise.
        """
        try:
            await self.get_by_id(exercise_id)  # Checking if exercise exists
            deleted = await self.delete(exercise_id)
            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error on deleting exercise with id: {exercise_id}",
                )
            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content={"message": "Exercise deleted"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error on deleting exercise with id: {exercise_id}",
            )
