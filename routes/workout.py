from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.authentication import AuthenticationRequired

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.post("/")
async def create_new_workout_plan():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


@router.get("/")
async def get_workout_plans():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


@router.get("/{workout_id}")
async def get_workout_plan(workout_id: int):
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
