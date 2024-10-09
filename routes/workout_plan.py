from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.workout_plan import WorkoutPlanCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.workout_plan import WorkoutPlanCreate, WorkoutPlanUpdate, WorkoutPlanPartialUpdate

router: APIRouter = APIRouter(
    dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_workout_plans_api(skip: int = 0, limit: int = 10,
                                session: AsyncSession = Depends(get_async_session)):
    workout_plan_crud: WorkoutPlanCrud = WorkoutPlanCrud(session)
    return await workout_plan_crud.get_all(skip=skip, limit=limit)


@router.get("/{workout_plan_id}")
async def get_workout_plan_api(workout_plan_id: int, session: AsyncSession = Depends(get_async_session)):
    workout_plan_crud: WorkoutPlanCrud = WorkoutPlanCrud(session)
    return await workout_plan_crud.get_workout_plan_by_id(workout_plan_id)


@router.post("/")
async def create_workout_plan_api(workout_plan_data: WorkoutPlanCreate,
                                  session: AsyncSession = Depends(get_async_session)):
    workout_plan_crud: WorkoutPlanCrud = WorkoutPlanCrud(session)
    return await workout_plan_crud.create_workout_plan(workout_plan_data.model_dump())



@router.patch("/{workout_plan_id}")
async def partial_update_workout_plan_api(workout_plan_id: int, workout_plan_data: WorkoutPlanPartialUpdate,
                                          session: AsyncSession = Depends(get_async_session)):
    workout_plan_crud: WorkoutPlanCrud = WorkoutPlanCrud(session)
    return await workout_plan_crud.update_workout_plan(workout_plan_id, workout_plan_data.model_dump(exclude_none=True))


@router.delete("/{workout_plan_id}")
async def delete_workout_plan_id(workout_plan_id: int, session: AsyncSession = Depends(get_async_session)):
    workout_plan_crud: WorkoutPlanCrud = WorkoutPlanCrud(session)
    await workout_plan_crud.delete_workout_plan(workout_plan_id)
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={
                            "message": "Workout plan deleted successfully"
                                       ""
                        })
