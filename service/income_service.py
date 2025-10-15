from models.income_models import IncomeAdd, IncomeRead, IncomeUpdate
from repository.income_repository import IncomeRepository


class IncomeService:
    def __init__(self, repository: IncomeRepository) -> None:
        self.__repository = repository

    def create_income(self, income_add: IncomeAdd) -> IncomeRead:
        return IncomeRead.model_validate(self.__repository.add(income_add))

    def get_income(self, income_id: int) -> IncomeRead:
        return IncomeRead.model_validate(self.__repository.get_one(income_id))

    def get_all_incomes(self, skip:int, limit:int) -> list[IncomeRead]:
        return [
            IncomeRead.model_validate(income) for income in self.__repository.get_all(skip, limit)
        ]

    def delete_income(self, income_id: int) -> bool:
        return self.__repository.delete(income_id)

    def update_income(self, income_to_update: IncomeUpdate) -> IncomeRead:
        return IncomeRead.model_validate(
            self.__repository.update(income_to_update.id, income_to_update)
        )
