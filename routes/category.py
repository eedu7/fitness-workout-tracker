from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.category import CategoryCrud
from db import get_async_session
from dependencies.authentication import AuthenticationRequired
from schemas.category import (CategoryCreateData, CategoryPartialUpdateData,
                              CategoryUpdateData)

router: APIRouter = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get(
    "/",
    summary="Get all categories",
    description="Retrieve a list of all categories with pagination.",
)
async def get_all_categories_api(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a paginated list of all categories.

    - **skip**: Number of records to skip (default: 0).
    - **limit**: Maximum number of records to return (default: 10).

    Returns:
        A list of categories limited by the `skip` and `limit` parameters.
    """
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.get_all_categories(skip, limit)


@router.get(
    "/{category_id}",
    summary="Get category by ID",
    description="Retrieve a specific category by its ID.",
)
async def get_category_by_id_api(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a specific category by its ID.

    - **category_id**: The ID of the category to retrieve.

    Returns:
        The details of the specified category, or an error if not found.
    """
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.get_category_by_id(category_id)


@router.post(
    "/",
    summary="Create a new category",
    description="Create a new category with the provided data.",
)
async def create_new_category_api(
    category_data: CategoryCreateData,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Create a new category.

    - **category_data**: The data required to create a new category.

    Returns:
        The newly created category data.
    """
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.create_category(**category_data.model_dump())


@router.put(
    "/{category_id}",
    summary="Update a category",
    description="Update an existing category by its ID.",
)
async def update_category_api(
    category_id: int,
    category_data: CategoryUpdateData,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Update an existing category with the provided full data.

    - **category_id**: The ID of the category to update.
    - **category_data**: The new data for the category.

    Returns:
        The updated category data, or an error if the category is not found.
    """
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.update_category(
        category_id, **category_data.model_dump()
    )


@router.patch(
    "/{category_id}",
    summary="Partially update a category",
    description="Update certain fields of an existing category by its ID.",
)
async def update_category_api(
    category_id: int,
    category_data: CategoryPartialUpdateData,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Partially update an existing category with the provided data.

    - **category_id**: The ID of the category to update.
    - **category_data**: The partial data for the category.

    Returns:
        The updated category data, or an error if the category is not found.
    """
    category_crud: CategoryCrud = CategoryCrud(session)
    return await category_crud.update_category(
        category_id, **category_data.model_dump()
    )


@router.delete(
    "/{category_id}",
    summary="Delete a category",
    description="Delete a category by its ID.",
)
async def delete_category_api(
    category_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a category by its ID.

    - **category_id**: The ID of the category to delete.

    Returns:
        A success message indicating the category was deleted successfully or an error message if deletion fails.
    """
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
