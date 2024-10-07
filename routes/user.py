from fastapi import APIRouter, HTTPException, status, Depends
from select import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db import get_async_session
from models import User
from schemas.user import UserRegister, UserResponse

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_users(skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    """
    Fetch a list of users with optional pagination.

    Parameters:
    - skip: The number of records to skip (default: 0)
    - limit: The maximum number of records to return (default: 10)

    Returns:
    - A list of user records.
    """
    result = await session.execute(select(User).offset(skip).limit(limit))
    users = result.scalars().all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found.")

    return users


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserRegister, session: AsyncSession = Depends(get_async_session)):
    """
    Create a new user in the database.


    Parameters:
    - user_data: Data required to register a user (name, email, password)

    Returns:
    - The created user data (id, name, email).
    """
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=user_data.password  # Be sure to hash this password in a real app
    )

    session.add(new_user)

    try:
        await session.commit()
        await session.refresh(new_user)  # Refresh to get the generated ID
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    return new_user
