from typing import Annotated
from fastapi import APIRouter, Path
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise import ExerciseCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.exercise import ExerciseCreate, ExerciseUpdate, ExercisePartialUpdate

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_all_exercise(
        skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_all_exercise(skip, limit)


@router.get("/{exercise_id}")
async def get_exercise(exercise_id: Annotated[int, Path(ge=1)], session: AsyncSession = Depends(get_async_session)):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_by_id(exercise_id)


@router.post("/")
async def create_new_exercise(
        exercise_data: ExerciseCreate, session: AsyncSession = Depends(get_async_session)
):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.create_exercise(**exercise_data.model_dump())


@router.put("/{exercise_id}")
async def update_exercise(exercise_id: Annotated[int, Path(ge=1)], exercise_data: ExerciseUpdate,
                          session: AsyncSession = Depends(get_async_session)):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.update_exercise(exercise_id, **exercise_data.model_dump())


@router.patch("/{exercise_id}")
async def partial_update_exercise(exercise_id: Annotated[int, Path(ge=1)], exercise_data: ExercisePartialUpdate,
                                  session: AsyncSession = Depends(get_async_session)):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.update_exercise(exercise_id, **exercise_data.model_dump(exclude_none=True))



@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: Annotated[int, Path(ge=1)], session: AsyncSession= Depends(get_async_session)):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.delete_exercise(exercise_id)
