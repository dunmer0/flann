from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.schemas import Period
from models.period_models import PeriodToAdd, PeriodToUpdate


class PeriodRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, period_to_add: PeriodToAdd) -> Period:
        period = Period(**period_to_add.model_dump())
        self.session.add(period)
        self.session.commit()
        self.session.refresh(period)
        return period

    def get_by_id(self, period_id: int) -> Optional[Period]:
        return self.session.get(Period, period_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Period]:
        statement = select(Period).offset(skip).limit(limit)
        return list(self.session.scalars(statement))

    def update(
        self, period_id: int, period_update: PeriodToUpdate
    ) -> Optional[Period]:
        db_period = self.get_by_id(period_id)
        if not db_period:
            return db_period
        update_data = period_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_period, key, value)

        self.session.commit()
        self.session.refresh(db_period)
        return db_period

    def delete(self, period_id: int) -> bool:
        db_period = self.get_by_id(period_id)
        if not db_period:
            return False
        self.session.delete(db_period)
        self.session.commit()
        return True
