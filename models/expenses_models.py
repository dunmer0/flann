from pydantic import BaseModel, ConfigDict


class ExpenseAdd(BaseModel):
    name: str
    amount: float
    category_id: int
    model_config = ConfigDict(from_attributes=True)


class ExpenseUpdate(BaseModel):
    id: int
    name: str
    amount: float
    model_config = ConfigDict(from_attributes=True)


class ExpenseRead(BaseModel):
    id: int
    name: str
    amount: float
    model_config = ConfigDict(from_attributes=True)
