from typing import List

from models.expenses_models import ExpenseAdd, ExpenseRead, ExpenseUpdate
from repository.category_repository import CategoryRepository
from repository.expenses_repository import ExpensesRepository
from repository.repository_exceptions import RepositoryError
from service.service_exception import ServiceException


class ExpenseService:
    def __init__(
        self, expense_repo: ExpensesRepository, category_repo: CategoryRepository
    ):
        self.expense_repo = expense_repo
        self.category_repo = category_repo

    def add_expense(self, expense: ExpenseAdd) -> ExpenseRead:
        category = self.category_repo.get_category(expense.category_id)
        if not category:
            raise ServiceException(f"Category with id:{expense.category_id} not found")
        try:
            return ExpenseRead.model_validate(self.expense_repo.add_expense(expense))
        except RepositoryError as e:
            raise ServiceException(f"Could not add expense {str(e)}")

    def get_expense(self, expense_id: int) -> ExpenseRead:
        expense = ExpenseRead.model_validate(self.expense_repo.get_expense(expense_id))
        if not expense:
            raise ServiceException(f"Expense with id:{expense_id} not found")
        return expense

    def get_expenses(self, skip: int, limit: int) -> list[ExpenseRead]:
        return [
            ExpenseRead.model_validate(expense)
            for expense in self.expense_repo.get_all_expenses(skip, limit)
        ]

    def get_expenses_by_category(self, category_id: int) -> List[ExpenseRead]:
        return [
            ExpenseRead.model_validate(expense)
            for expense in self.expense_repo.get_expenses_by_category_id(category_id)
        ]

    def update_expense(self, expense_update: ExpenseUpdate) -> ExpenseRead:
        expense_db = self.expense_repo.get_expense(expense_update.id)
        if not expense_db:
            raise ServiceException(f"Expense with id:{expense_update.id} not found")
        return ExpenseRead.model_validate(
            self.expense_repo.update_expense(expense_db, expense_update)
        )

    def delete_expense(self, expense_id: int) -> bool:
        expense = self.expense_repo.get_expense(expense_id)
        if not expense:
            raise ServiceException(f"Expense with id:{expense_id} not found")
        self.expense_repo.delete_expense(expense)
        return True
