from datetime import date

from pydantic import BaseModel, ConfigDict


class IncomeAdd(BaseModel):
    name: str
    amount: float
    date: date
    period_id: int

    model_config = ConfigDict(from_attributes=True)


class IncomeRead(BaseModel):
    id: int
    amount: float
    name: str
    date: date

    model_config = ConfigDict(from_attributes=True)


class IncomeUpdate(BaseModel):
    id: int
    name: str
    amount: float
    date: date

    model_config = ConfigDict(from_attributes=True)
