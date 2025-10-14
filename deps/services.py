from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from repository.period_repository import PeriodRepository
from service.period_service import PeriodService
from .database import SessionDep



def get_period_repository(session:SessionDep)-> PeriodRepository:
    return PeriodRepository(session)

PeriodRepositoryDep = Annotated[PeriodRepository, Depends(get_period_repository)]

def get_period_service(repository:PeriodRepositoryDep)-> PeriodService:
    return PeriodService(repository)

PeriodServiceDep = Annotated[PeriodService, Depends(get_period_service)]