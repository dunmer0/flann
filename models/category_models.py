from pydantic import BaseModel, ConfigDict


class CategoryAdd(BaseModel):
    name: str
    anticipated_expense: float
    period_id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(BaseModel):
    id: int
    name: str
    anticipated_expense: float

    model_config = ConfigDict(from_attributes=True)


class CategoryRead(BaseModel):
    id: int
    name: str
    anticipated_expense: float
    actual_expenses: float = 0
    period_id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryNameDTO(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
