from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from config import config
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from models import User
from schemas.user import UserLogin, UserRegister, UserResponse
from utils.jwt_handler import encode_token
from utils.password import hash_password, verify_password

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

    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()

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
    existing_user = await session.execute(select(User).filter_by(email=user_data.email))
    if existing_user.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered."
        )

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password),
    )

    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists.",
        )

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
    - A message indicating successful login and a token
    """
    existing_user = await session.execute(select(User).filter_by(email=user_data.email))
    user = existing_user.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not registered."
        )

    if not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
        )

    return {
        "message": "Login successful",
        "token": {
            "access_token": encode_token(
                {"user_id": user.id},
            ),
            "refresh_token": encode_token(
                {"user_id": user.id, "sub": "refresh"},
            ),
        },
    }
