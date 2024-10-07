from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from .user import router as user_router

app = FastAPI(
    title="Fitness Workout Tracker",
    version="1.0.0",
)


@app.get("/")
async def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Title": "Fitness Workout Tracker",
            "Version": "1.0.0",
        },
    )


app.include_router(user_router, prefix="/user", tags=["User"])
