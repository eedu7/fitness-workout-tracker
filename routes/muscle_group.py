from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.muscle_group import MuscleGroupCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.muscle_group import (MuscleGroupCreate, MuscleGroupPartialUpdate,
                                  MuscleGroupUpdate)

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get(
    "/",
    summary="Get all muscle groups",
    description="Retrieve a list of all muscle groups with pagination.",
)
async def get_all_muscle_groups_api(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a paginated list of all muscle groups.

    - **skip**: Number of records to skip (default: 0).
    - **limit**: Maximum number of records to return (default: 10).

    Returns:
        A list of muscle groups limited by the `skip` and `limit` parameters.
    """
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.get_all_muscle_group(skip=skip, limit=limit)


@router.get(
    "/{muscle_group_id}",
    summary="Get muscle group by ID",
    description="Retrieve a specific muscle group by its ID.",
)
async def get_muscle_group_by_id_api(
    muscle_group_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a specific muscle group by its ID.

    - **muscle_group_id**: The ID of the muscle group to retrieve.

    Returns:
        The details of the specified muscle group, or an error if not found.
    """
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.get_muscle_group_by_id(muscle_group_id)


@router.post(
    "/",
    summary="Create a new muscle group",
    description="Create a new muscle group with the provided data.",
)
async def create_muscle_group_api(
    muscle_group_data: MuscleGroupCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new muscle group.

    - **muscle_group_data**: The data required to create a new muscle group.

    Returns:
        The newly created muscle group data.
    """
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.create_muscle_group(**muscle_group_data.model_dump())


@router.put(
    "/{muscle_group_id}",
    summary="Update a muscle group",
    description="Update an existing muscle group by its ID.",
)
async def update_muscle_group_api(
    muscle_group_id: int,
    muscle_group_data: MuscleGroupUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an existing muscle group with the provided full data.

    - **muscle_group_id**: The ID of the muscle group to update.
    - **muscle_group_data**: The new data for the muscle group.

    Returns:
        The updated muscle group data, or an error if the muscle group is not found.
    """
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.update_muscle_group(
        muscle_group_id, **muscle_group_data.model_dump()
    )


@router.patch(
    "/{muscle_group_id}",
    summary="Partially update a muscle group",
    description="Update certain fields of an existing muscle group by its ID.",
)
async def partial_update_muscle_group_api(
    muscle_group_id: int,
    muscle_group_data: MuscleGroupPartialUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Partially update an existing muscle group with the provided data.

    - **muscle_group_id**: The ID of the muscle group to update.
    - **muscle_group_data**: The partial data for the muscle group.

    Returns:
        The updated muscle group data, or an error if the muscle group is not found.
    """
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.update_muscle_group(
        muscle_group_id, **muscle_group_data.model_dump(exclude_none=True)
    )


@router.delete(
    "/{muscle_group_id}",
    summary="Delete a muscle group",
    description="Delete a muscle group by its ID.",
)
async def delete_muscle_group_api(
    muscle_group_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a muscle group by its ID.

    - **muscle_group_id**: The ID of the muscle group to delete.

    Returns:
        A success message indicating the muscle group was deleted successfully or an error message if deletion fails.
    """
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    deleted = await muscle_group_crud.delete_muscle_group(muscle_group_id)
    if not deleted:
        return JSONResponse(
            status_code=400,
            content={"status": "error", "message": "Error deleting muscle group"},
        )
    return JSONResponse(
        status_code=200,
        content={"status": "success", "message": "Muscle group deleted successfully"},
    )
