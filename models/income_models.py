from datetime import date

# class Income(Base):
#     __tablename__ = "incomes"
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     amount: Mapped[float] = mapped_column(Float, nullable=False)
#     date: Mapped[date] = mapped_column(Date, nullable=False)
#     period_id: Mapped[int] = mapped_column(ForeignKey("period.id",ondelete="CASCADE"))

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
