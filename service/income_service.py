from models.income_models import IncomeAdd, IncomeRead, IncomeUpdate
from repository.category_repository import CategoryRepository
from repository.income_repository import IncomeRepository
from service.service_exception import ServiceException


class IncomeService:
    def __init__(self, income_repository: IncomeRepository, category_repository: CategoryRepository) -> None:
        self.__income_repository = income_repository
        self.__category_repository = category_repository

    def create_income(self, income_add: IncomeAdd) -> IncomeRead:
        income_db = self.__category_repository.get_category(income_add.category_id)
        if not income_db:
            raise ServiceException("Category not found")
        return IncomeRead.model_validate(self.__income_repository.add(income_add))

    def get_income(self, income_id: int) -> IncomeRead:
        return IncomeRead.model_validate(self.__income_repository.get_one(income_id))

    def get_all_incomes(self, skip:int, limit:int) -> list[IncomeRead]:
        return [
            IncomeRead.model_validate(income) for income in self.__income_repository.get_all(skip, limit)
        ]

    def delete_income(self, income_id: int) -> None:
        return self.__income_repository.delete(income_id)

    def update_income(self, income_to_update: IncomeUpdate) -> IncomeRead:
        return IncomeRead.model_validate(
            self.__income_repository.update(income_to_update.id, income_to_update)
        )
