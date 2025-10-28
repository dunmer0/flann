from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.schemas import Category
from models.category_models import CategoryAdd, CategoryUpdate
from repository.repository_exceptions import RepositoryError


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_category(self, category_data: CategoryAdd) -> Category:
        category = Category(**category_data.model_dump())
        try:
            self.session.add(category)
            self.session.commit()
            self.session.refresh(category)
            return category
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not add category {str(e)}") from e

    def get_category(self, category_id: int) -> Optional[Category]:
        return self.session.get(Category, category_id)

    def get_categories(self, skip: int, limit: int) -> list[Category]:
        return list(
            self.session.scalars(statement=select(Category).offset(skip).limit(limit))
        )

    def update_category(
        self, category: Category, update_data: CategoryUpdate
    ) -> Category:
        """
        Update a category
        """
        self.session.merge(category)
        update_model = update_data.model_dump(exclude_unset=True)
        for key, value in update_model:
            setattr(category, key, value)
        try:
            self.session.commit()
            self.session.refresh(category)
            return category
        except SQLAlchemyError as e:
            raise RepositoryError(f"Could not update category {str(e)}") from e

    def delete_category(self, category: Category):
        try:
            self.session.delete(category)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not delete the category {str(e)}") from e
