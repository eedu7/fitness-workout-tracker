from typing import Annotated
from fastapi import APIRouter, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise import ExerciseCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.exercise import ExerciseCreate, ExerciseUpdate, ExercisePartialUpdate

# router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])
router: APIRouter = APIRouter()


@router.get("/")
async def get_all_exercise(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    """
    Get a list of all exercises with pagination.

    Args:
        skip (int): The number of records to skip. Default is 0.
        limit (int): The maximum number of records to return. Default is 10.
        session (AsyncSession): The async database session. Automatically injected by FastAPI.

    Returns:
        List of exercises limited by the `skip` and `limit` parameters.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_all_exercise(skip, limit)


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_async_session)):
    """
    Get details of a specific exercise by its ID.

    Args:
        exercise_id (int): The ID of the exercise. Must be greater than or equal to 1.
        session (AsyncSession): The async database session. Automatically injected by FastAPI.

    Returns:
        The details of the exercise with the given `exercise_id`, or an error if not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_by_id(exercise_id)


@router.post("/")
async def create_new_exercise(exercise_data: ExerciseCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new exercise.

    Args:
        exercise_data (ExerciseCreate): The data required to create a new exercise.
        session (AsyncSession): The async database session. Automatically injected by FastAPI.

    Returns:
        The newly created exercise data.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.create_exercise(**exercise_data.model_dump())


@router.put("/{exercise_id}")
async def update_exercise(
    exercise_id: Annotated[int, Path(ge=1)],
    exercise_data: ExerciseUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing exercise with full data replacement.

    Args:
        exercise_id (int): The ID of the exercise to update. Must be greater than or equal to 1.
        exercise_data (ExerciseUpdate): The new data for the exercise.
        session (AsyncSession): The async database session. Automatically injected by FastAPI.

    Returns:
        The updated exercise data, or an error if the exercise is not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.update_exercise(exercise_id, **exercise_data.model_dump())


@router.patch("/{exercise_id}")
async def partial_update_exercise(
    exercise_id: Annotated[int, Path(ge=1)],
    exercise_data: ExercisePartialUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Partially update an existing exercise with the provided data.

    Args:
        exercise_id (int): The ID of the exercise to update. Must be greater than or equal to 1.
        exercise_data (ExercisePartialUpdate): The partial data to update the exercise.
        session (AsyncSession): The async database session. Automatically injected by FastAPI.

    Returns:
        The updated exercise data, or an error if the exercise is not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.update_exercise(exercise_id, **exercise_data.model_dump(exclude_none=True))


@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_async_session)):
    """
    Delete an exercise by its ID.

    Args:
        exercise_id (int): The ID of the exercise to delete. Must be greater than or equal to 1.
        session (AsyncSession): The async database session. Automatically injected by FastAPI.

    Returns:
        Success message or an error if the exercise is not found.
    """
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.delete_exercise(exercise_id)
