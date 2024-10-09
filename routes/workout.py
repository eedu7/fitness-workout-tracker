from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from crud.workout import WorkoutCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.workout import WorkoutCreate, WorkoutUpdate, WorkoutPartialUpdate

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/", summary="Get all workout plans", description="Retrieve a list of all workout plans with pagination.")
async def get_workout_plans(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve a paginated list of all workout plans.

    - **skip**: Number of records to skip (default: 0).
    - **limit**: Maximum number of records to return (default: 10).

    Returns:
        A list of workout plans limited by the `skip` and `limit` parameters.
    """
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.get_all(skip=skip, limit=limit)


@router.get("/{workout_id}", summary="Get a workout plan", description="Retrieve details of a specific workout plan by its ID.")
async def get_workout_plan(workout_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve the details of a specific workout plan by its ID.

    - **workout_id**: The ID of the workout plan.

    Returns:
        The details of the workout plan, or an error if not found.
    """
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.get_workout_by_id(workout_id)


@router.post("/", summary="Create a new workout plan", description="Create a new workout plan with the provided data.")
async def create_new_workout_plan(workout_data: WorkoutCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new workout plan.

    - **workout_data**: The data required to create a new workout plan.

    Returns:
        The newly created workout plan data.
    """
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.create_workout(workout_data.model_dump())


@router.put("/{workout_id}", summary="Update a workout plan", description="Update an existing workout plan by its ID.")
async def update_workout_plan(workout_id: int, workout_data: WorkoutUpdate,
                              session: AsyncSession = Depends(get_async_session)):
    """
    Update an existing workout plan with the provided full data.

    - **workout_id**: The ID of the workout plan to update.
    - **workout_data**: The new data for the workout plan.

    Returns:
        The updated workout plan data, or an error if the workout plan is not found.
    """
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.update_workout(workout_id, workout_data.model_dump())


@router.patch("/{workout_id}", summary="Partially update a workout plan", description="Update certain fields of an existing workout plan by its ID.")
async def partial_update_workout_plan(workout_id: int, workout_data: WorkoutPartialUpdate,
                                      session: AsyncSession = Depends(get_async_session)):
    """
    Partially update an existing workout plan with the provided data.

    - **workout_id**: The ID of the workout plan to update.
    - **workout_data**: The partial data for the workout plan.

    Returns:
        The updated workout plan data, or an error if the workout plan is not found.
    """
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.update_workout(workout_id, workout_data.model_dump(exclude_none=True))


@router.delete("/{workout_id}", summary="Delete a workout plan", description="Delete a workout plan by its ID.")
async def delete_workout_plan(workout_id: int, session: AsyncSession = Depends(get_async_session)):
    """
    Delete a workout plan by its ID.

    - **workout_id**: The ID of the workout plan to delete.

    Returns:
        A success message indicating the workout plan was deleted successfully.
    """
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    await workout_crud.delete_workout(workout_id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Workout deleted successfully!"
        }
    )
