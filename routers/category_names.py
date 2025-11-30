from fastapi.routing import APIRouter

from deps import CategoryNameServiceDep
from models.category_models import CategoryNameDTO

router = APIRouter()


@router.post(path="/", response_model=CategoryNameDTO)
def add_category_name(service: CategoryNameServiceDep, category_name: str):
    return service.add_category_name(category_name)


@router.put(path="/", response_model=CategoryNameDTO)
def update_category_name(
    service: CategoryNameServiceDep, category_name: CategoryNameDTO
):
    return service.update_category_name(category_name)


@router.get(path="/", response_model=list[CategoryNameDTO])
def get_all_category_name(
    service: CategoryNameServiceDep, skip: int = 0, limit: int = 10
) -> list[CategoryNameDTO]:
    return service.get_all_category_name(skip, limit)


@router.get(path="/by-id/{category_name_id}", response_model=CategoryNameDTO)
def get_category_name_by_id(
    service: CategoryNameServiceDep, category_name_id: int
) -> CategoryNameDTO:
    return service.get_category_name_by_id(category_name_id)


@router.get(path="/by-name/{category_name_name}", response_model=CategoryNameDTO)
def get_category_name_by_name(
    service: CategoryNameServiceDep, category_name_name: str
) -> CategoryNameDTO:
    return service.get_category_name_by_name(category_name_name)


@router.delete(path="/{category_name_id}", response_model=None)
def delete_category_name(
    service: CategoryNameServiceDep, category_name_id: int
) -> None:
    service.delete_category_name(category_name_id)
