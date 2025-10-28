from models.category_models import CategoryAdd, CategoryRead, CategoryUpdate
from repository.category_repository import CategoryRepository
from repository.repository_exceptions import RepositoryError
from service.service_exception import ServiceException


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def add_category(self, category: CategoryAdd) -> CategoryRead:
        category_db = self.repository.add_category(
            category_data=category
        )
        return CategoryRead.model_validate(category_db)

    def get_category(self, category_id: int) -> CategoryRead:
        category_db = self.repository.get_category(category_id)

        if not category_db:
            raise ServiceException(
                f"There is no category with id: {category_id}"
            )
        category = CategoryRead.model_validate(category_db, from_attributes=True)
        for expense in category_db.expenses:
            category.actual_expenses += expense.cost
        return category

    def get_categories(
            self, skip: int = 0, limit: int = 10
    ) -> list[CategoryRead]:
        return [
            CategoryRead.model_validate(category)
            for category in self.repository.get_categories(
                skip=skip, limit=limit
            )
        ]

    def update_category(self, category_update: CategoryUpdate) -> CategoryRead:
        category_db = self.repository.get_category(
            category_id=category_update.id
        )
        if not category_db:
            raise ServiceException(
                f"There is no category with id: {category_update.id}"
            )
        try:
            return CategoryRead.model_validate(
                self.repository.update_category(
                    category=category_db,
                    update_data=category_update.model_dump(exclude_unset=True),
                ),
                from_attributes=True,
            )
        except RepositoryError as e:
            raise ServiceException(
                f"Could not update the entity. {str(e)}"
            ) from e

    def delete_category(self, category_id: int) -> bool:
        category_db = self.repository.get_category(category_id=category_id)
        if not category_db:
            return False
        try:
            self.repository.delete_category(category=category_db)
            return True
        except RepositoryError as e:
            raise ServiceException(
                f"Could not delete the entity. {str(e)}"
            ) from e
