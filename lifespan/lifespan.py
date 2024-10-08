import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_async_session
from models import Category, MuscleGroup

BASE_DIR = Path(__file__).resolve().parent


async def seed_categories(db: AsyncSession):
    """
    Seed categories asynchronously if they don't exist.
    """
    CATEGORIES = BASE_DIR / "seeds/category.json"

    with open(CATEGORIES, "r") as file:
        categories = json.load(file)

    for category in categories:
        db_category = Category(**category)
        await db.merge(db_category)

    await db.commit()


async def seed_muscle_group(db: AsyncSession):
    """
    Seed muscle groups asynchronously if they don't exist.
    """
    MUSCLE_GROUPS = BASE_DIR / "seeds/muscle_group.json"
    with open(MUSCLE_GROUPS, "r") as file:
        muscle_groups = json.load(file)

    for muscle_group in muscle_groups:
        db_muscle_group = MuscleGroup(**muscle_group)
        await db.merge(db_muscle_group)

    await db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create a session and seed data during app startup
    async with get_async_session() as db:
        await seed_categories(db)
        await seed_muscle_group(db)
