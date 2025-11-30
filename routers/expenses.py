from fastapi import APIRouter

from deps import ExpenseServiceDep
from models.expenses_models import ExpenseRead, ExpenseAdd, ExpenseUpdate

router = APIRouter()


@router.post(path="/", response_model=ExpenseRead)
def add_expense(expense_service: ExpenseServiceDep,
                expense_add: ExpenseAdd) -> ExpenseRead:
    return expense_service.add_expense(expense_add)


@router.put(path="/", response_model=ExpenseRead)
def update_expense(expense_service: ExpenseServiceDep,
                   expense_update: ExpenseUpdate) -> ExpenseRead:
    return expense_service.update_expense(expense_update)


@router.get(path="/", response_model=list[ExpenseRead])
def get_expenses(expense_service: ExpenseServiceDep):
    return expense_service.get_expenses()


@router.get(path="/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_service: ExpenseServiceDep, expense_id: int) -> ExpenseRead:
    return expense_service.get_expense(expense_id)


@router.delete(path="{expense_id}")
def delete_expense(expense_service: ExpenseServiceDep, expense_id: int) -> bool:
    return expense_service.delete_expense(expense_id)
