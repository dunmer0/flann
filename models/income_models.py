from datetime import date
# class Income(Base):
#     __tablename__ = "incomes"
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     amount: Mapped[float] = mapped_column(Float, nullable=False)
#     date: Mapped[date] = mapped_column(Date, nullable=False)
#     period_id: Mapped[int] = mapped_column(ForeignKey("period.id",ondelete="CASCADE"))

from pydantic import BaseModel


class IncomeAdd(BaseModel):
    name: str
    amount: float
    date: date
    period_id: int
    
class IncomeRead(BaseModel):
    name: str
    amount: float
    date: date