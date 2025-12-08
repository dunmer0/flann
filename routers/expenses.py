from typing import List

from fastapi import APIRouter

from deps import ExpenseServiceDep
from models.expenses_models import ExpenseAdd, ExpenseRead, ExpenseUpdate

router = APIRouter()


@router.post(path="/", response_model=ExpenseRead)
def add_expense(
    expense_service: ExpenseServiceDep, expense_add: ExpenseAdd
) -> ExpenseRead:
    return expense_service.add_expense(expense_add)


@router.put(path="/", response_model=ExpenseRead)
def update_expense(
    expense_service: ExpenseServiceDep, expense_update: ExpenseUpdate
) -> ExpenseRead:
    return expense_service.update_expense(expense_update)


@router.get(path="/", response_model=list[ExpenseRead])
def get_expenses(
    expense_service: ExpenseServiceDep, skip: int = 0, limit: int = 10
) -> List[ExpenseRead]:
    return expense_service.get_expenses(skip=skip, limit=limit)


@router.get(path="/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_service: ExpenseServiceDep, expense_id: int) -> ExpenseRead:
    return expense_service.get_expense(expense_id)


@router.get(path="/category/{category_id}", response_model=List[ExpenseRead])
def get_expenses_by_category(
    expense_service: ExpenseServiceDep, category_id: int
) -> List[ExpenseRead]:
    return expense_service.get_expenses_by_category(category_id)


@router.delete(path="/{expense_id}")
def delete_expense(expense_service: ExpenseServiceDep, expense_id: int) -> bool:
    return expense_service.delete_expense(expense_id)
