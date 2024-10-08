from dataclasses import field
from typing import Any, List

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCrud
from models import MuscleGroup


class MuscleGroupCrud(BaseCrud[MuscleGroup]):
    """CRUD operations for MuscleGroup model."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the MuscleGroupCrud with an async database session.

        Args:
            session (AsyncSession): An async SQLAlchemy session for database interactions.
        """
        super().__init__(MuscleGroup, session)

    async def get_all_muscle_group(
        self, skip: int = 0, limit: int = 20
    ) -> List[MuscleGroup]:
        """Retrieve all muscle groups with optional pagination.

        Args:
            skip (int): The number of records to skip (for pagination). Default is 0.
            limit (int): The maximum number of records to return. Default is 20.

        Returns:
            List[MuscleGroup]: A list of MuscleGroup instances.

        Raises:
            HTTPException: If no muscle groups are found, a 404 error is raised.
        """
        try:
            muscle_groups = await super().get_all(skip, limit)
            if not muscle_groups:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No muscle groups found",
                )
            return muscle_groups
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on fetching all muscle groups: {str(e)}",
            )

    async def get_muscle_group_by_id(self, muscle_group_id: int) -> MuscleGroup:
        """Retrieve a muscle group by its ID.

        Args:
            muscle_group_id (int): The ID of the muscle group.

        Returns:
            MuscleGroup: The muscle group instance if found.

        Raises:
            HTTPException: If the muscle group is not found, a 404 error is raised.
        """
        try:
            muscle_group: MuscleGroup = await super().get_by_id(muscle_group_id)
            if not muscle_group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No muscle group found with ID: {muscle_group_id}",
                )
            return muscle_group
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on fetching muscle group: {str(e)}",
            )

    async def get_by_name(self, name: str) -> MuscleGroup:
        """Retrieve a muscle group by its name.

        Args:
            name (str): The name of the muscle group.

        Returns:
            MuscleGroup: The muscle group instance if found.

        Raises:
            HTTPException: If the muscle group is not found, a 404 error is raised.
        """
        try:
            muscle_group: MuscleGroup = await self.get_by(field="name", value=name)
            if not muscle_group:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No muscle group found with name: {name}",
                )
            return muscle_group
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on fetching muscle group: {str(e)}",
            )

    async def create_muscle_group(self, name: str, description: str) -> MuscleGroup:
        """Create a new muscle group.

        Args:
            name (str): The name of the muscle group.
            description (str): A description of the muscle group.

        Returns:
            MuscleGroup: The newly created muscle group instance.

        Raises:
            HTTPException: If a muscle group with the same name already exists, a 400 error is raised.
            HTTPException: If an error occurs during the creation process, a 500 error is raised.
        """
        try:
            muscle_group: MuscleGroup = await self.get_by(field="name", value=name)
            if muscle_group:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Muscle group already exists with name: {name}",
                )
            new_muscle_group: MuscleGroup = await self.create(
                {"name": name, "description": description}
            )
            return new_muscle_group
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on creating muscle group: {str(e)}",
            )

    async def update_muscle_group(
        self,
        muscle_group_id: int,
        name: str | None = None,
        description: str | None = None,
    ) -> MuscleGroup:
        """Update an existing muscle group.

        Args:
            muscle_group_id (int): The ID of the muscle group to update.
            name (str): The new name of the muscle group.
            description (str): The new description of the muscle group.

        Returns:
            MuscleGroup: The updated muscle group instance.

        Raises:
            HTTPException: If the muscle group is not found, a 404 error is raised.
            HTTPException: If an error occurs during the update process, a 500 error is raised.
        """
        try:
            await self.get_by_id(muscle_group_id)  # Checking if muscle group exists
            data = {}

            if name:
                data["name"] = name
            if description:
                data["description"] = description

            updated_muscle_group = await self.update(muscle_group_id, data)

            return updated_muscle_group
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on updating muscle group: {str(e)}",
            )

    async def delete_muscle_group(self, muscle_group_id: int) -> JSONResponse:
        """Delete a muscle group by its ID.

        Args:
            muscle_group_id (int): The ID of the muscle group to delete.

        Returns:
            JSONResponse: A response indicating the muscle group was successfully deleted.

        Raises:
            HTTPException: If the muscle group is not found, a 404 error is raised.
            HTTPException: If an error occurs during the deletion process, a 500 error is raised.
        """
        try:
            await self.get_by_id(muscle_group_id)  # Check to see if muscle group exists

            await self.delete(muscle_group_id)

            return JSONResponse(
                status_code=status.HTTP_202_ACCEPTED,
                content={"message": "Muscle group deleted"},
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on deleting muscle group: {str(e)}",
            )
