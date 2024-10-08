from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCrud
from models import Category


class CategoryCrud(BaseCrud[Category]):
    """
    A CRUD (Create, Read, Update, Delete) interface for managing Category entities.

    Inherits from BaseCrud, providing methods to interact with the Category model in the database.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Initializes the CategoryCrud instance.

        Parameters:
        - session (AsyncSession): An instance of SQLAlchemy's AsyncSession to perform database operations.
        """
        super().__init__(model=Category, session=session)

    async def get_all_categories(
        self, skip: int = 0, limit: int = 10
    ) -> list[Category]:
        """
        Retrieves all categories from the database, with optional pagination.

        Parameters:
        - skip (int): The number of categories to skip (for pagination). Default is 0.
        - limit (int): The maximum number of categories to return. Default is 10.

        Returns:
        - list[Category]: A list of Category objects.

        Raises:
        - HTTPException: If no categories are found (404) or on server error (500).
        """
        try:
            categories = await self.get_all(skip=skip, limit=limit)
            if not categories:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No categories found",
                )
            return categories
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on fetching categories: {e}",
            )

    async def get_category_by_id(self, category_id: int) -> Category:
        """
        Retrieves a category by its ID.

        Parameters:
        - category_id (int): The ID of the category to retrieve.

        Returns:
        - Category: The Category object with the specified ID.

        Raises:
        - HTTPException: If the category is not found (404) or on server error (500).
        """
        try:
            category: Category = await self.get_by_id(category_id)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with ID: {category_id} not found",
                )
            return category
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on fetching category. {e}",
            )

    async def get_category_by_name(self, category_name: str) -> Category:
        """
        Retrieves a category by its name.

        Parameters:
        - category_name (str): The name of the category to retrieve.

        Returns:
        - Category: The Category object with the specified name.

        Raises:
        - HTTPException: If the category is not found (404) or on server error (500).
        """
        try:
            category: Category = await self.get_by(field="name", value=category_name)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with name: {category_name} not found",
                )
            return category
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on fetching category. {e}",
            )

    async def create_category(self, name: str, description: str) -> Category:
        """
        Creates a new category in the database.

        Parameters:
        - name (str): The name of the new category.
        - description (str): A description of the new category.

        Returns:
        - Category: The newly created Category object.

        Raises:
        - HTTPException: If a category with the same name already exists (400) or on server error (500).
        """
        try:
            category = await self.get_by(field="name", value=name)
            if category:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Category with name: {name} already exists",
                )
            new_category = await self.create(
                {
                    "name": name,
                    "description": description,
                }
            )
            return new_category
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on creating category. {e}",
            )

    async def update_category(
        self, category_id: int, name: str, description: str
    ) -> Category:
        """
        Updates an existing category in the database.

        Parameters:
        - category_id (int): The ID of the category to update.
        - name (str): The new name of the category (optional).
        - description (str): The new description of the category (optional).

        Returns:
        - Category: The updated Category object.

        Raises:
        - HTTPException: If the category does not exist (404) or on server error (500).
        """
        try:
            await self.get_category_by_id(category_id)
            data = {}
            if name:
                data["name"] = name
            if description:
                data["description"] = description

            updated_category = await self.update(category_id, data)
            return updated_category
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on updating category. {e}",
            )

    async def delete_category(self, category_id: int) -> bool:
        """
        Deletes a category from the database.

        Parameters:
        - category_id (int): The ID of the category to delete.

        Returns:
        - JSONResponse: A response indicating successful deletion (204 No Content).

        Raises:
        - HTTPException: If the category does not exist (404) or on server error (500).
        """
        try:
            await self.get_category_by_id(category_id)

            deleted = await self.delete(category_id)
            if deleted:
                return True
            return False
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error on deleting category. {e}",
            )
