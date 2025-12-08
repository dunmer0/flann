from typing import List

from db.schemas import Category
from models.category_models import CategoryAdd, CategoryRead, CategoryUpdate
from repository.category_repository import CategoryRepository
from repository.period_repository import PeriodRepository
from repository.repository_exceptions import RepositoryError
from service.service_exception import ServiceException


class CategoryService:
    def __init__(
            self, category_repo: CategoryRepository, period_repo: PeriodRepository,
            # category_name_repo: CategoryNameRepository
    ) -> None:
        self.category_repo = category_repo
        self.period_repo = period_repo
        # self.category_name_repo = category_name_repo

    def add_category(self, category: CategoryAdd) -> CategoryRead:
        period = self.period_repo.get_by_id(category.period_id)
        # category_name = self.category_name_repo.get_category_name(
        #     category.category_name_id)
        if not period:
            raise ServiceException(f"There is no period with id: {category.period_id}")
        # if not category_name:
        #     raise ServiceException(
        #         f"There is no category name: {category.category_name_id}")
        category_db = self.category_repo.add_category(Category(**category.model_dump()))
        return CategoryRead.model_validate(category_db)

    def get_category(self, category_id: int) -> CategoryRead:
        category_db = self.category_repo.get_category_with_expenses(category_id)
        if not category_db:
            raise ServiceException(f"There is no category with id: {category_id}")
        category = CategoryRead.from_category(category_db)
        for expense in category_db.expenses:
            category.actual_expenses += expense.cost
        return category

    # def get_categories(self, skip: int = 0, limit: int = 10) -> list[CategoryRead]:
    #     return [
    #         CategoryRead.from_category(category)
    #         for category in self.category_repo.get_categories(skip=skip, limit=limit)
    #     ]

    def get_categories(self, skip: int = 0, limit: int = 100) -> List[CategoryRead]:
        categories_db = self.category_repo.get_categories(skip=skip, limit=limit)
        result: list[CategoryRead] = []
        for category_db in categories_db:
            category = CategoryRead.from_category(category_db)
            category.actual_expenses = sum(
                expense.cost for expense in category_db.expenses)
            result.append(category)
        return result

    def update_category(self, category_update: CategoryUpdate) -> CategoryRead:
        category_db = self.category_repo.get_category(category_id=category_update.id)
        if not category_db:
            raise ServiceException(
                f"There is no category with id: {category_update.id}"
            )
        try:
            return CategoryRead.model_validate(
                self.category_repo.update_category(category_db, category_update)
            )
        except RepositoryError as e:
            raise ServiceException(f"Could not update the entity. {str(e)}") from e

    def delete_category(self, category_id: int) -> bool:
        category_db = self.category_repo.get_category(category_id=category_id)
        if not category_db:
            return False
        try:
            self.category_repo.delete_category(category=category_db)
            return True
        except RepositoryError as e:
            raise ServiceException(f"Could not delete the entity. {str(e)}") from e
