from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

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


        }
    )
