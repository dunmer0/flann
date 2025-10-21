from fastapi import APIRouter

from deps import CategoryServiceDep
from models.category_models import CategoryAdd, CategoryRead, CategoryUpdate

router = APIRouter()


@router.post(path="/", response_model=CategoryRead)
def add_category(
    service: CategoryServiceDep, category_add: CategoryAdd
) -> CategoryRead:
    return service.add_category(category=category_add)


@router.put(path="/", response_model=CategoryRead)
def update_category(
    service: CategoryServiceDep, category_update: CategoryUpdate
) -> CategoryRead:
    return service.update_category(category_update=category_update)


@router.get(path="/", response_model=list[CategoryRead])
def get_categories(
    service: CategoryServiceDep, skip: int, limit: int
) -> list[CategoryRead]:
    return service.get_categories(skip, limit)


@router.get(path="/{category_id}", response_model=CategoryRead)
def get_category(
    service: CategoryServiceDep, category_id: int
) -> CategoryRead:
    return service.get_category(category_id=category_id)


@router.delete(path="/{category_id}", response_model=bool)
def delete_category(service: CategoryServiceDep, category_id: int) -> bool:
    return service.delete_category(category_id=category_id)
