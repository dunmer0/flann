from db.schemas import CategoryName
from models.category_models import CategoryNameDTO
from repository.category_name_repository import CategoryNameRepository
from repository.repository_exceptions import RepositoryError
from service.service_exception import ServiceException


class CategoryNameService:
    def __init__(self, category_name_repo: CategoryNameRepository) -> None:
        self.__category_name_repo = category_name_repo

    def add_category_name(self, category_name: str) -> CategoryNameDTO:
        # category_to_add = CategoryName(name=category_name
        try:
            return CategoryNameDTO.model_validate(
                self.__category_name_repo.add_category_name(
                    CategoryName(name=category_name)
                )
            )
        except RepositoryError as e:
            raise ServiceException(f"{str(e)}") from e

    def get_category_name_by_id(self, category_name_id: int) -> CategoryNameDTO:
        category_name = self.__category_name_repo.get_category_name(category_name_id)
        if not category_name:
            raise ServiceException(
                f"Could not find category_name with id: {category_name_id}"
            )
        return CategoryNameDTO.model_validate(category_name)

    def get_category_name_by_name(self, category_name_name: str) -> CategoryNameDTO:
        category_name = self.__category_name_repo.get_category_name_by_name(
            category_name_name
        )
        if not category_name:
            raise ServiceException(
                f"Could not find category_name with name: {category_name_name}"
            )
        return CategoryNameDTO.model_validate(category_name)

    def get_all_category_name(self, skip: int, limit: int) -> list[CategoryNameDTO]:
        return [
            CategoryNameDTO.model_validate(category_name)
            for category_name in self.__category_name_repo.get_all_category_name(
                skip, limit
            )
        ]

    def update_category_name(self, category_name: CategoryNameDTO) -> CategoryNameDTO:
        category_name_db = self.__category_name_repo.get_category_name(category_name.id)
        if not category_name_db:
            raise ServiceException(
                f"Could not find category_name with id: {category_name.id}"
            )
        try:
            return CategoryNameDTO.model_validate(
                self.__category_name_repo.update_category_name(
                    category_name_db, category_name
                )
            )
        except RepositoryError as e:
            raise ServiceException(
                f"Error occured while trying to update: {str(e)}"
            ) from e

    def delete_category_name(self, category_name_id: int) -> None:
        category_name_db = self.__category_name_repo.get_category_name(category_name_id)
        if not category_name_db:
            raise ServiceException(
                f"Could not find category_name with id: {category_name_id}"
            )
        try:
            self.__category_name_repo.delete_category_name(category_name_db)
        except RepositoryError as e:
            raise ServiceException(f"Could not delete category_name: {str(e)}") from e
