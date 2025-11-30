from datetime import date
from typing import List

from sqlalchemy import Date, Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base):
    __tablename__ = "users"
    name: Mapped[str] = mapped_column(String, nullable=False)


class Period(Base):
    __tablename__ = "period"
    start: Mapped[date] = mapped_column(Date, nullable=False)
    end: Mapped[date] = mapped_column(Date, nullable=False)

    categories: Mapped[list["Category"]] = relationship(backref="period")


class Income(Base):
    __tablename__ = "incomes"
    name: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    added: Mapped[date] = mapped_column(Date, nullable=False)
    period_id: Mapped[int] = mapped_column(ForeignKey("period.id", ondelete="CASCADE"))

class CategoryName(Base):
    __tablename__= "category_names"

    name: Mapped[str] = mapped_column(String, nullable=False)

class Category(Base):
    __tablename__ = "categories"

    category_name: Mapped[int] = mapped_column(ForeignKey("category_names.id"))
    anticipated_expense: Mapped[float] = mapped_column(Float, nullable=True)
    period_id: Mapped[int] = mapped_column(ForeignKey("period.id", ondelete="CASCADE"))

    expenses: Mapped[List["Expense"]] = relationship(backref="category")


class Expense(Base):
    __tablename__ = "expenses"
    name: Mapped[str] = mapped_column(String, nullable=False)
    cost: Mapped[float] = mapped_column(Float, nullable=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE")
    )
