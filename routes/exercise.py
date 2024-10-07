from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from dependencies.authentication import AuthenticationRequired
from schemas.exercise import ExerciseCreate

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/")
async def get_all_exercise():
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


@router.get("/{exercise_id}")
async def get_exercise(exercise_id):
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Not Implemented",
    )


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
