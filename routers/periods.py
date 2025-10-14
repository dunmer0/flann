from fastapi import APIRouter

from deps import PeriodServiceDep
from models.period_models import PeriodRead, PeriodToAdd, PeriodToUpdate

router = APIRouter()

@router.post("/", response_model=PeriodRead)
def create_period(period_add: PeriodToAdd, service:PeriodServiceDep):
    return service.create_period(period_add)

@router.put("/")
def update_period(service:PeriodServiceDep, period_to_update: PeriodToUpdate):
    return service.update_period(period_to_update)

@router.get("/")
def get_all_periods(service:PeriodServiceDep, skip:int = 0, limit: int = 100):
    return service.get_all_periods(skip, limit)


@router.get("/{period_id}")
def get_one_period(service:PeriodServiceDep, period_id:int):
    return service.get_period(period_id)

@router.delete("/{period_id}")
def delete_one_period(service:PeriodServiceDep, period_id:int):
    return service.delete_period(period_id)