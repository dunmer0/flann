from typing import Annotated

from fastapi import Depends

from repository.category_name_repository import CategoryNameRepository
from repository.category_repository import CategoryRepository
from repository.expenses_repository import ExpensesRepository
from repository.income_repository import IncomeRepository
from repository.period_repository import PeriodRepository
from service.category_name_service import CategoryNameService
from service.category_service import CategoryService
from service.expenses_service import ExpenseService
from service.income_service import IncomeService
from service.period_service import PeriodService

from .database import SessionDep

# Respositories


def get_period_repository(session: SessionDep) -> PeriodRepository:
    return PeriodRepository(session)


PeriodRepositoryDep = Annotated[PeriodRepository, Depends(get_period_repository)]


def get_category_repository(session: SessionDep) -> CategoryRepository:
    return CategoryRepository(session=session)


CategoryRepositoryDep = Annotated[CategoryRepository, Depends(get_category_repository)]


def get_income_repository(session: SessionDep) -> IncomeRepository:
    return IncomeRepository(session)


IncomeRepositoryDep = Annotated[IncomeRepository, Depends(get_income_repository)]


def get_expense_repository(session: SessionDep):
    return ExpensesRepository(session=session)


ExpensesRepositoryDep = Annotated[ExpensesRepository, Depends(get_expense_repository)]


def get_category_name_repository(session: SessionDep):
    return CategoryNameRepository(session=session)


CategoryNameRepositoryDep = Annotated[
    CategoryNameRepository, Depends(get_category_name_repository)
]


# Services


def get_period_service(repository: PeriodRepositoryDep) -> PeriodService:
    return PeriodService(repository)


PeriodServiceDep = Annotated[PeriodService, Depends(get_period_service)]


def get_income_service(
    income_repo: IncomeRepositoryDep, category_repo: CategoryRepositoryDep
) -> IncomeService:
    return IncomeService(income_repo, category_repo)


IncomeServiceDep = Annotated[IncomeService, Depends(get_income_service)]


def get_category_service(
    category_repo: CategoryRepositoryDep,
    period_repo: PeriodRepositoryDep,
    category_name_repo: CategoryNameRepositoryDep,
) -> CategoryService:
    return CategoryService(
        category_repo=category_repo,
        period_repo=period_repo,
        category_name_repo=category_name_repo,
    )


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]


def get_expense_service(
    expense_repo: ExpensesRepositoryDep, category_repo: CategoryRepositoryDep
):
    return ExpenseService(expense_repo, category_repo)


ExpenseServiceDep = Annotated[ExpenseService, Depends(get_expense_service)]


def get_cateogry_name_service(category_name_repo: CategoryNameRepositoryDep):
    return CategoryNameService(category_name_repo)


CategoryNameServiceDep = Annotated[
    CategoryNameService, Depends(get_cateogry_name_service)
]
