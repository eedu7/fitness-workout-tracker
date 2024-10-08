from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.muscle_group import MuscleGroupCrud
from db import get_async_session
from schemas.muscle_group import (MuscleGroupCreate, MuscleGroupPartialUpdate,
                                  MuscleGroupUpdate)

# TODO: added Authentication
router: APIRouter = APIRouter()


@router.get("/")
async def get_all_muscle_groups_api(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.get_all_muscle_group(skip=skip, limit=limit)


@router.get("/{muscle_group_id}")
async def get_muscle_group_by_id_api(
    muscle_group_id: int, session: AsyncSession = Depends(get_async_session)
):
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.get_muscle_group_by_id(muscle_group_id)


@router.post("/")
async def create_muscle_group_api(
    muscle_group_data: MuscleGroupCreate,
    session: AsyncSession = Depends(get_async_session),
):
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.create_muscle_group(**muscle_group_data.model_dump())


@router.put("/{muscle_group_id}")
async def update_muscle_group_api(
    muscle_group_id: int,
    muscle_group_data: MuscleGroupUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.update_muscle_group(
        muscle_group_id, **muscle_group_data.model_dump()
    )


@router.patch("/{muscle_group_id}")
async def partial_update_muscle_group_api(
    muscle_group_id: int,
    muscle_group_data: MuscleGroupPartialUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.update_muscle_group(
        muscle_group_id, **muscle_group_data.model_dump(exclude_none=True)
    )


@router.delete("/{muscle_group_id}")
async def delete_muscle_group_api(
    muscle_group_id: int, session: AsyncSession = Depends(get_async_session)
):
    muscle_group_crud: MuscleGroupCrud = MuscleGroupCrud(session)
    return await muscle_group_crud.delete_muscle_group(muscle_group_id)
