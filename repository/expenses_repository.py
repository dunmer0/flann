from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.schemas import Expense
from models.expenses_models import ExpenseAdd, ExpenseUpdate
from repository.repository_exceptions import RepositoryError


class ExpensesRepository:
    def __init__(self, session: Session):
        self.session = session

    def add_expense(self, expense_add: ExpenseAdd) -> Expense:
        """
        Add an expense even if it already exists.
        Args:
            expense_add (ExpenseAdd): Expense to add
        Returns:
            Expense: Expense
        Raises:
            RepositoryError: if adding fails

        """
        expense = Expense(**expense_add.model_dump())
        try:
            self.session.add(expense)
            self.session.commit()
            self.session.refresh(expense)
            return expense
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not add expense: {str(e)}") from e

    def get_expense(self, expense_id: int) -> Optional[Expense]:
        """
        Get expense by id
        Args:
            expense_id (int): expense id
        Returns:
            Optional[Expense]: expense object or none
        """
        return self.session.get(Expense, expense_id)

    def get_all_expenses(self, skip: int, limit: int) -> list[Expense]:
        """
        Get all expenses
        Args:
            skip (int): skip count
            limit (int): limit count
        Returns:
            list[Expense]: expense objects or empty list
        """
        return list(
            self.session.scalars(statement=select(Expense).offset(skip).limit(limit)))

    def update_expense(self, expense: Expense, update_data: ExpenseUpdate) -> Expense:
        """
        Update an expense
        Args:
            expense (Expense): expense to update
            update_data (ExpenseUpdate): update data for expense
        Returns:
            Expense: expense object
        Raises:
            RepositoryError: if updating fails
        """
        self.session.merge(expense)
        update_model = update_data.model_dump(exclude_unset=True)
        for key, value in update_model.items():
            setattr(self, key, value)
        try:
            self.session.commit()
            self.session.refresh(expense)
            return expense
        except SQLAlchemyError as e:
            raise RepositoryError(f"Could not update expense: {str(e)}") from e

    def delete_expense(self, expense: Expense) -> None:
        """
        Delete an expense
        Args:
            expense (Expense): expense to delete
        Returns:
            None
        """
        try:
            self.session.delete(expense)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not delete expense: {str(e)}") from e
