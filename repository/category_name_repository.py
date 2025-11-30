from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.schemas import CategoryName
from models.category_models import CategoryNameDTO
from repository.repository_exceptions import RepositoryError


class CategoryNameRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_category_name(self, category_name: CategoryName) -> CategoryName:
        try:
            self.session.add(category_name)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not add category name {str(e)}") from e
        else:
            self.session.refresh(category_name)
            return category_name

    def get_category_name(self, category_name_id: int) -> Optional[CategoryName]:
        print("something")
        return self.session.get(CategoryName, category_name_id)

    def get_category_name_by_name(
        self, category_name_name: str
    ) -> Optional[CategoryName]:
        stmt = select(CategoryName).where(CategoryName.name == category_name_name)

        return self.session.scalar(stmt)

    def get_all_category_name(self, skip: int, limit: int) -> list[CategoryName]:
        return list(
            self.session.scalars(
                statement=select(CategoryName).offset(skip).limit(limit)
            )
        )

    def update_category_name(
        self, category_name: CategoryName, update_data: CategoryNameDTO
    ) -> CategoryName:
        self.session.merge(category_name)
        update_model = update_data.model_dump(exclude_unset=True)
        for key, value in update_model.items():
            setattr(category_name, key, value)
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            raise RepositoryError(f"Could not upadate category_name {str(e)}") from e

        self.session.refresh(category_name)
        return category_name

    def delete_category_name(self, category: CategoryName) -> None:
        try:
            self.session.delete(category)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not delete category_name {str(e)}") from e
        else:
            self.session.commit()
