from sys import get_asyncgen_hooks

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from crud.workout import WorkoutCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])




@router.get("/")
async def get_workout_plans(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.get_all(skip=skip, limit=limit)


@router.get("/{workout_id}")
async def get_workout_plan(workout_id: int, session: AsyncSession = Depends(get_async_session)):
    workout_crud: WorkoutCrud = WorkoutCrud(session)
    return await workout_crud.get_workout_by_id(workout_id)

@router.post("/")
async def create_new_workout_plan():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


@router.put("/{workout_id}")
async def update_workout_plan(workout_id: int):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


@router.delete("/{workout_id}")
async def delete_workout_plan(workout_id: int):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )
