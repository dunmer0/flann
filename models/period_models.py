from pydantic import BaseModel, ConfigDict
from datetime import date


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