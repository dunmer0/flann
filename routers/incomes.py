from http.client import SERVICE_UNAVAILABLE
from fastapi import APIRouter
from deps import IncomeServiceDep
from models import IncomeAdd, IncomeRead, IncomeUpdate


router = APIRouter()


@router.post(path="/", response_model=IncomeRead)
def add_income(service: IncomeServiceDep, income_add: IncomeAdd) -> IncomeRead:
    return service.create_income(income_add)


@router.put(path="/", response_model=IncomeRead)
def update_income(service: IncomeServiceDep, income_update: IncomeUpdate) -> IncomeRead:
    return service.update_income(income_update)


@router.get(path="/{income_id}", response_model=IncomeRead)
def get_income(service: IncomeServiceDep, income_id: int) -> IncomeRead:
    return service.get_income(income_id)


@router.get(path="/", response_model=list[IncomeRead])
def get_all_incomes(
    service: IncomeServiceDep, skip: int, limit: int
) -> list[IncomeRead]:
    return service.get_all_incomes(skip, limit)


@router.delete(path="/{income_id}", response_model=bool)
def delete_income(service: IncomeServiceDep, income_id: int) -> bool:
    return service.delete_income(income_id)
