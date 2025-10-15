from typing import Optional, List

from models.period_models import PeriodToAdd, PeriodRead, PeriodToUpdate
from repository.period_repository import PeriodRepository


class PeriodService:
    def __init__(self, repository: PeriodRepository):
        self.__repository = repository

    def create_period(self, period_create: PeriodToAdd) -> PeriodRead:

        db_period = self.__repository.add(period_create)
        return PeriodRead.model_validate(db_period)

    def get_period(self, period_id: int) -> PeriodRead:
        return PeriodRead.model_validate(self.__repository.get_by_id(period_id))

    def get_all_periods(self, skip: int = 0, limit: int = 100) -> list[PeriodRead]:
        return [PeriodRead.model_validate(period) for period in self.__repository.get_all(skip, limit)]

    def delete_period(self, period_id:int)->bool:
        return self.__repository.delete(period_id)

    def update_period(self, period_to_update:PeriodToUpdate)-> PeriodRead:
        return PeriodRead.model_validate(self.__repository.update(period_to_update.id, period_to_update))
