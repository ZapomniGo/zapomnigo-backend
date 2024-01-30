from typing import Tuple, Any, Dict

from flask import request
from ulid import ULID

from src.database.models import Categories
from src.database.repositories.categories_repository import CategoriesRepository
from src.database.repositories.common_repository import CommonRepository
from src.pydantic_models.categories_model import CategoriesModel, CategoriesWithSubcategoriesModel
from src.utilities.parsers import validate_json_body
from src.pydantic_models.categories_model import UpdateCategoriesModel


class CategoriesController:

    @classmethod
    def create_category(cls, json_data: CategoriesModel):
        return Categories(category_id=str(ULID()), category_name=json_data.category_name.strip())

    @classmethod
    def add_category(cls):
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, CategoriesModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_category(CategoriesModel(**json_data)))

        return {"message": "Category added to db"}, 200

    @classmethod
    def get_all_categories(cls) -> Tuple[Dict[str, Any], int]:
        if result := CommonRepository.get_all_objects_from_db(Categories):
            return {"categories": [categories.to_json() for categories in result]}, 200

        return {"message": "No categories were found"}, 404

    @classmethod
    def get_category(cls, category_id: str) -> Tuple[Dict[str, Any], int]:
        if category := CategoriesRepository.get_category_by_id(category_id):
            return {"category": category.to_json()}, 200

        return {"message": "Category with such id doesn't exist"}, 404

    @classmethod
    def update_category(cls, category_id: str):
        json_data = request.get_json()
        category = CategoriesRepository.get_category_by_id(category_id)

        if not category:
            return {"message": "Category with such id doesn't exist"}, 404

        if validation_errors := validate_json_body(json_data, UpdateCategoriesModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.edit_object(category, CategoriesModel(**json_data))
        return {"message": "Category successfully updated"}, 200

    @classmethod
    def delete_category(cls, category_id: str) -> Tuple[Dict[str, Any], int]:
        if category := CategoriesRepository.get_category_by_id(category_id):
            CommonRepository.delete_object_from_db(category)
            return {"message": "Category successfully deleted"}, 200

        return {"message": "Category with such id doesn't exist"}, 404
    @classmethod
    def create_folder_sets(cls, set_ids: List[str], folder_obj_id: str) -> List[FoldersSets]:
        folder_sets_objects = []
        for set_id in set_ids:
            folder_sets_objects.append(FoldersSets(folder_set_id=str(ULID()), folder_id=folder_obj_id, set_id=set_id))

        return folder_sets_objects
    @classmethod
    def create_subcategories_for_category(cls, category_id: str, json_data: CategoriesWithSubcategoriesModel):
        return