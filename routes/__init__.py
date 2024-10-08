from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from middleware.authentication import AuthBackend, AuthenticationMiddleware

from .category import router as category_router
from .exercise import router as exercise_router
from .user import router as user_router
from .workout import router as workout_router

app = FastAPI(
    title="Fitness Workout Tracker",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())


@app.get("/")
async def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "status": "success",
            "data": {
                "title": "Fitness Workout Tracker",
                "version": "1.0.0",
            },
        },
    )


@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy"},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": str(exc)},
    )


# Register routes
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(workout_router, prefix="/workout", tags=["Workout Management"])
app.include_router(exercise_router, prefix="/exercise", tags=["Exercise"])
app.include_router(category_router, prefix="/category", tags=["Category"])
