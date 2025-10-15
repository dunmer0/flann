from typing import Annotated

from fastapi import Depends

from repository.income_repository import IncomeRepository
from repository.period_repository import PeriodRepository
from service.income_service import IncomeService
from service.period_service import PeriodService

from .database import SessionDep


def get_period_repository(session: SessionDep) -> PeriodRepository:
    return PeriodRepository(session)


PeriodRepositoryDep = Annotated[PeriodRepository, Depends(get_period_repository)]


def get_period_service(repository: PeriodRepositoryDep) -> PeriodService:
    return PeriodService(repository)


PeriodServiceDep = Annotated[PeriodService, Depends(get_period_service)]


def get_income_repository(
    session: SessionDep, period_repository: PeriodRepositoryDep
) -> IncomeRepository:
    return IncomeRepository(session, period_repository)


IncomeRepositoryDep = Annotated[IncomeRepository, Depends(get_income_repository)]


def get_income_service(repository: IncomeRepositoryDep) -> IncomeService:
    return IncomeService(repository)


IncomeServiceDep = Annotated[IncomeService, Depends(get_income_service)]
