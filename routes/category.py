from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.category import CategoryCrud
from db import get_async_session
from schemas.category import (CategoryCreateData, CategoryPartialUpdateData,
                              CategoryUpdateData)

# TODO: add authentication required dependency
router: APIRouter = APIRouter()


@router.get("/")
async def get_all_categories_api(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.get_all_categories(skip, limit)


@router.get("/{category_id}")
async def get_category_by_id_api(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.get_category_by_id(category_id)


@router.post("/")
async def create_new_category_api(
    category_data: CategoryCreateData,
    session: AsyncSession = Depends(get_async_session),
):
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.create_category(**category_data.model_dump())


@router.put("/{category_id}")
async def update_category_api(
    category_id: int,
    category_data: CategoryUpdateData,
    session: AsyncSession = Depends(get_async_session),
):
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.update_category(
        category_id, **category_data.model_dump()
    )


@router.patch("/{category_id}")
async def update_category_api(
    category_id: int,
    category_data: CategoryPartialUpdateData,
    session: AsyncSession = Depends(get_async_session),
):
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.update_category(
        category_id, **category_data.model_dump()
    )


@router.delete("/{category_id}")
async def delete_category_api(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    category_crud: CategoryCrud = CategoryCrud(session)
    deleted = await category_crud.delete_category(category_id)
    if not deleted:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content="Error on deleting category",
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success", "message": "Category deleted successfully"},
    )
