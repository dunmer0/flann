from typing import List

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Date, Float, String, ForeignKey
from datetime import date


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String, nullable=False)


class Period(Base):
    __tablename__ = "period"
    start: Mapped[date] = mapped_column(Date, nullable=False)
    end: Mapped[date] = mapped_column(Date, nullable=False)

    incomes: Mapped[List["Income"]] = relationship(backref="period")
    expenses: Mapped[List["Expense"]] = relationship(backref="period")


class Income(Base):
    __tablename__ = "incomes"
    name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("period.id",ondelete="CASCADE"))


class Catergory(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String, nullable=False)
    anticipated_expensed: Mapped[float] = mapped_column(Float, nullable=False)
    actual_expenses: Mapped[float] = mapped_column(Float)

    expenses: Mapped[List["Expense"]] = relationship(backref="category")


class Expense(Base):
    __tablename__ = "expenses"
    name: Mapped[str] = mapped_column(String, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("period.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
