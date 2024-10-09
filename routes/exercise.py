from typing import Annotated

from fastapi import APIRouter, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise import ExerciseCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.exercise import ExerciseCreate, ExerciseUpdate, ExercisePartialUpdate

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/", summary="Get all exercises", description="Retrieve a list of all exercises with pagination.")
async def get_all_exercise(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    """
    Retrieves a paginated list of all exercises.

    - **skip**: Number of records to skip (default: 0).
    - **limit**: Maximum number of records to return (default: 10).

    Returns:
        A list of exercises limited by the `skip` and `limit` parameters.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_all_exercise(skip, limit)


@router.get("/{exercise_id}", summary="Get an exercise",
            description="Retrieve details of a specific exercise by its ID.")
async def get_exercise(exercise_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_async_session)):
    """
    Retrieve the details of a specific exercise by its ID.

    - **exercise_id**: The ID of the exercise. Must be greater than or equal to 1.

    Returns:
        The details of the exercise, or an error if not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_by_id(exercise_id)


@router.post("/", summary="Create a new exercise", description="Create a new exercise with the provided data.")
async def create_new_exercise(exercise_data: ExerciseCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new exercise.

    - **exercise_data**: The data required to create a new exercise.

    Returns:
        The newly created exercise data.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.create_exercise(**exercise_data.model_dump())


@router.put("/{exercise_id}", summary="Update an exercise", description="Update an existing exercise by its ID.")
async def update_exercise(
        exercise_id: Annotated[int, Path(ge=1)],
        exercise_data: ExerciseUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing exercise with the provided full data.

    - **exercise_id**: The ID of the exercise to update.
    - **exercise_data**: The new data for the exercise.

    Returns:
        The updated exercise data, or an error if the exercise is not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.update_exercise(exercise_id, **exercise_data.model_dump())


@router.patch("/{exercise_id}", summary="Partially update an exercise",
              description="Update certain fields of an existing exercise by its ID.")
async def partial_update_exercise(
        exercise_id: Annotated[int, Path(ge=1)],
        exercise_data: ExercisePartialUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """
    Partially update an existing exercise with the provided data.

    - **exercise_id**: The ID of the exercise to update.
    - **exercise_data**: The partial data for the exercise.

    Returns:
        The updated exercise data, or an error if the exercise is not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.update_exercise(exercise_id, **exercise_data.model_dump(exclude_none=True))


@router.delete("/{exercise_id}", summary="Delete an exercise", description="Delete an exercise by its ID.")
async def delete_exercise(exercise_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_async_session)):
    """
    Delete an exercise by its ID.

    - **exercise_id**: The ID of the exercise to delete.

    Returns:
        A success message, or an error if the exercise is not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.delete_exercise(exercise_id)
