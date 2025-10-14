from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Optional, List

from db.schemas import Income
from models.income_models import IncomeAdd, IncomeUpdate
from repository.period_repository import PeriodRepository


class IncomeRepository:
    def __init__(self, session: Session, period_repository: PeriodRepository) -> None:
        self.session = session
        self.period_repository = period_repository

    def add(self, income_add: IncomeAdd) -> Optional[Income]:
        db_period = self.period_repository.get_by_id(income_add.period_id)
        if db_period is None:
            return None
        new_income = Income(**income_add.model_dump())
        try:
            db_period.incomes.append(new_income)
            self.session.add(new_income)
            self.session.commit()
            self.session.refresh(new_income)
            return new_income
        except Exception as e:
            self.session.rollback()
            raise Exception("Could not add entity: {str(e)}") from e

    def get_one(self, income_id: int) -> Optional[Income]:
        return self.session.get(Income, income_id)  # type: ignore

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Income]:
        return list(
            self.session.scalars(statement=select(Income).offset(skip).limit(limit))
        )

    def update(self, income_id: int, income_update: IncomeUpdate) -> Optional[Income]:
        db_income = self.get_one(income_id)
        if db_income:
            return None
        update_data = income_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_income, key, value)

        self.session.commit()
        self.session.refresh(db_income)
        return db_income

    def delete(self, income_id: int) -> bool:
        db_income = self.get_one(income_id)
        if not db_income:
            return False
        db_period = self.period_repository.get_by_id(db_income.period_id)
        if not  db_period:
            return False

        try:
            self.session.delete(db_income)
            db_period.incomes.remove(db_income)
            self.session.commit()
            self.session.refresh(db_period)
            return True
        except Exception as e:
            self.session.rollback()
            raise Exception(f"could not delete entity {str(e)}") from e
