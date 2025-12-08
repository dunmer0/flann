from pydantic import BaseModel, ConfigDict

from db.schemas import Category


class CategoryAdd(BaseModel):
    anticipated_expense: float
    period_id: int
    category_name_id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(BaseModel):
    id: int
    category_name_id: int
    anticipated_expense: float

    model_config = ConfigDict(from_attributes=True)


class CategoryRead(BaseModel):
    id: int
    name: str
    anticipated_expense: float
    actual_expenses: float = 0
    period_id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    @classmethod
    def from_category(cls, category: Category):
        data = category.__dict__.copy()
        data["name"] = category.category_name.name
        return cls.model_validate(data)


class CategoryNameDTO(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)
