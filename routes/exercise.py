from sys import get_asyncgen_hooks

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from crud.exercise import ExerciseCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.exercise import ExerciseCreate

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_all_exercise(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_all_exercise(skip, limit)


@router.get("/{exercise_id}")
async def get_exercise(exercise_id, session: AsyncSession = Depends(get_async_session)):
    exercise_crud: ExerciseCrud = ExerciseCrud(session)
    return await exercise_crud.get_by_id(exercise_id)

class ExerciseData(BaseModel):
    ...

@router.post("/")
async def create_new_exercise(exercise_data: ExerciseCreate):
    return exercise_data


@router.post("/{exercise_id}")
async def post_exercise(exercise_id: int):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


@router.delete("/{exercise_id}")
async def delete_exercise(exercise_id: int):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )
