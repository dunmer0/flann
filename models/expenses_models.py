from datetime import date

from pydantic import BaseModel, ConfigDict


class ExpenseAdd(BaseModel):
    name: str
    cost: float
    date: date
    category_id: int
    model_config = ConfigDict(from_attributes=True)


class ExpenseUpdate(BaseModel):
    id: int
    name: str
    cost: float
    date: date
    model_config = ConfigDict(from_attributes=True)


class ExpenseRead(BaseModel):
    id: int
    name: str
    cost: float
    date: date | None
    model_config = ConfigDict(from_attributes=True)
