from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import config
from crud.user import UserCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.user import UserLogin, UserRegister, UserResponse

router: APIRouter = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserResponse],
    dependencies=[Depends(AuthenticationRequired)],
)
async def get_users(
    skip: Annotated[int, Query(description="Number of records to skip")] = 0,
    limit: Annotated[
        int,
        Query(
            description=f"Maximum number of records to return. Max Limit is {config.PAGINATION_MAX_LIMIT}"
        ),
    ] = 10,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Fetch a list of users with optional pagination.

    Parameters:
    - skip: The number of records to skip (default: 0)
    - limit: The maximum number of records to return (default: 10)

    Returns:
    - A list of user records.
    """
    limit = min(limit, config.PAGINATION_MAX_LIMIT)
    user_crud = UserCrud(session=session)

    users = await user_crud.get_all(skip=skip, limit=limit)

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No users found."
        )

    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserRegister, session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new user in the database.

    Parameters:
    - user_data: Data required to register a user (name, email, password)

    Returns:
    - The created user data (id, name, email).
    """
    user_crud = UserCrud(session=session)

    try:
        new_user = await user_crud.register_user(user_data.dict())
    except HTTPException as e:
        raise e  # Re-raise the exception for proper error handling

    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(
    user_data: UserLogin, session: AsyncSession = Depends(get_async_session)
):
    """
    Login user by email and password.

    Parameters:
    - user_data: Data required for user login (email, password)

    Returns:
    - A message indicating successful login and a token.
    """
    user_crud = UserCrud(session=session)

    try:
        token = await user_crud.login_user(
            email=user_data.email, password=user_data.password
        )
    except HTTPException as e:
        raise e  # Re-raise the exception for proper error handling

    return {
        "message": "Login successful",
        "token": token,
    }
