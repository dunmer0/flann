from datetime import date

from pydantic import BaseModel, ConfigDict

from models.category_models import CategoryRead


class PeriodToAdd(BaseModel):
    start: date
    end: date

    model_config = ConfigDict(from_attributes=True)


class PeriodToUpdate(BaseModel):
    id: int
    start: date
    end: date

    model_config = ConfigDict(from_attributes=True)


class PeriodRead(BaseModel):
    id: int
    start: date
    end: date

    model_config = ConfigDict(from_attributes=True)


class PeriodReadWithCategories(BaseModel):
    id: int
    start: date
    end: date
    categories: list[CategoryRead]

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_period(cls, period):
        return cls.model_validate({
            "id": period.id,
            "start": period.start,
            "end": period.end,
            "categories": [CategoryRead.from_category(c) for c in period.categories],
        })
