from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.schemas import Period
from models.period_models import PeriodToAdd, PeriodToUpdate
from repository.repository_exceptions import RepositoryError


class PeriodRepository:
    def __init__(self, session: Session):

        self.session = session

    def add(self, period_to_add: PeriodToAdd) -> Period:
        """
        Add a period to the database

        Args:
            period_to_add (PeriodToAdd): Period to add

        Returns:
            PeriodToAdd: Period to add

       """
        period = Period(**period_to_add.model_dump())
        self.session.add(period)
        self.session.commit()
        self.session.refresh(period)
        return period

    def get_by_id(self, period_id: int) -> Optional[Period]:
        """
        Get a period by id
        Args:
            period_id (int): Period id
        Returns:
            Optional[Period]: Period or None
        """
        return self.session.get(Period, period_id)

    def get_all(self, skip: int, limit: int) -> List[Period]:
        """
        Get all periods
        Args:
            skip (int): Number of rows to skip
            limit (int): Number of rows to return
        Returns:
            List[Period]: List of periods
        """
        statement = select(Period).offset(skip).limit(limit)
        return list(self.session.scalars(statement))

    def update(
            self, period_id: int, period_update: PeriodToUpdate
    ) -> Period:
        """
        Update a period
        Args:
            period_id (int): Period id
            period_update (PeriodToUpdate): Period to update
        Returns:
            Period: Period
        Raises:
            RepositoryError: If update fails
        """
        db_period = self.get_by_id(period_id)
        if not db_period:
            raise RepositoryError(f"Period {period_id} not found")
        update_data = period_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_period, key, value)

        self.session.commit()
        self.session.refresh(db_period)
        return db_period

    def delete(self, period_id: int) -> None:
        """
        Delete a period
        Args:
            period_id (int): Period id
        Returns:
            None
        Raises:
            RepositoryError: If delete fails
        """
        db_period = self.get_by_id(period_id)
        if not db_period:
            raise RepositoryError(f"Period {period_id} not found")
        self.session.delete(db_period)
        self.session.commit()
