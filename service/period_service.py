from models.period_models import (
    PeriodRead,
    PeriodReadWithCategories,
    PeriodToAdd,
    PeriodToUpdate,
)
from repository.period_repository import PeriodRepository
from service.service_exception import ServiceException


class PeriodService:
    def __init__(self, repository: PeriodRepository):
        self.__repository = repository

    def create_period(self, period_create: PeriodToAdd) -> PeriodRead:
        db_period = self.__repository.add(period_create)
        return PeriodRead.model_validate(db_period)

    def get_period(self, period_id: int) -> PeriodRead:
        return PeriodRead.model_validate(self.__repository.get_by_id(period_id))

    # def get_period_with_categories(self, period_id: int) -> PeriodReadWithCategories:
    #     db_period = self.__repository.get_period_with_categories(period_id)

    #     if not db_period:
    #         raise ServiceException(f"Could not find period with id: {period_id}")

    #     return PeriodReadWithCategories.from_period(db_period)
    #
    def get_period_with_categories(self, period_id: int) -> PeriodReadWithCategories:
        db_period = self.__repository.get_period_with_categories(period_id)
        if not db_period:
            raise ServiceException(f"Could not find period with id: {period_id}")
        period_dto = PeriodReadWithCategories.from_period(db_period)

        for category_dto, category_db in zip(
            period_dto.categories, db_period.categories
        ):
            category_dto.actual_expenses = sum(
                expense.cost for expense in category_db.expenses
            )
        return period_dto

    def get_all_periods(self, skip: int = 0, limit: int = 10) -> list[PeriodRead]:
        return [
            PeriodRead.model_validate(period)
            for period in self.__repository.get_all(skip, limit)
        ]

    def delete_period(self, period_id: int) -> None:
        return self.__repository.delete(period_id)

    def update_period(self, period_to_update: PeriodToUpdate) -> PeriodRead:
        return PeriodRead.model_validate(
            self.__repository.update(period_to_update.id, period_to_update)
        )
