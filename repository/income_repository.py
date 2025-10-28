from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from db.schemas import Income
from models.income_models import IncomeAdd, IncomeUpdate
from repository.period_repository import PeriodRepository
from repository.repository_exceptions import RepositoryError


class IncomeRepository:
    def __init__(self, session: Session, period_repository: PeriodRepository) -> None:
        self.session = session
        # self.period_repository = period_repository

    def add(self, income_add: IncomeAdd) -> Income:
        new_income = Income(**income_add.model_dump())
        try:
            self.session.add(new_income)
            self.session.commit()
            self.session.refresh(new_income)
            return new_income
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"Could not add entity: {str(e)}") from e

    def get_one(self, income_id: int) -> Optional[Income]:
        return self.session.get(Income, income_id)  # type: ignore

    def get_all(self, skip: int, limit: int) -> List[Income]:
        return list(
            self.session.scalars(statement=select(Income).offset(skip).limit(limit))
        )

    def get_all_by_period(self, period_id: int, skip: int, limit: int) -> list[Income]:
        statement = (
            select(Income)
            .where(Income.period_id == period_id)
            .offset(skip)
            .limit(limit)
        )
        return list(self.session.scalars(statement))

    def update(self, income_id: int, income_update: IncomeUpdate) -> Income:
        db_income = self.get_one(income_id)
        if not db_income:
            raise RepositoryError(f"Income not found: {income_id}")
        update_data = income_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_income, key, value)
        self.session.commit()
        self.session.refresh(db_income)
        return db_income

    def delete(self, income_id: int) -> None:
        try:
            db_income = self.get_one(income_id)
            self.session.delete(db_income)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise RepositoryError(f"could not delete entity {str(e)}") from e
