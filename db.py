from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from config import config

engine = create_async_engine(config.MYSQL_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

