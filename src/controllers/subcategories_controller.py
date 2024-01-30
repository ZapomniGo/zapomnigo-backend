from typing import Tuple, Any, Dict

from flask import request
from ulid import ULID

from src.database.models import Categories, Subcategories
from src.database.repositories.categories_repository import CategoriesRepository
from src.database.repositories.common_repository import CommonRepository
from src.pydantic_models.categories_model import CategoriesModel, SubcategoriesModel
from src.utilities.parsers import validate_json_body
from src.pydantic_models.categories_model import UpdateCategoriesModel


class SubcategoriesController:

    @classmethod
    def create_subcategory(cls, json_data: SubcategoriesModel):
        return Subcategories(subcategory_id=str(ULID()), subcategory_name=json_data.subcategory_name.strip())

    @classmethod
    def add_subcategory(cls):
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, SubcategoriesModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_subcategory(SubcategoriesModel(**json_data)))

        return {"message": "Subcategory added to db"}, 200

    @classmethod
    def update_subcategory(cls, subcategory_id: str):
        json_data = request.get_json()
        subcategory = CategoriesRepository.get_subcategory_by_id(subcategory_id)

        if not subcategory:
            return {"message": "subcategory with such id doesn't exist"}, 404

        if validation_errors := validate_json_body(json_data, UpdateCategoriesModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.edit_object(subcategory, CategoriesModel(**json_data))
        return {"message": "subcategory successfully updated"}, 200

    @classmethod
    def delete_subcategory(cls, subcategory_id: str) -> Tuple[Dict[str, Any], int]:
        if subcategory := CategoriesRepository.get_subcategory_by_id(subcategory_id):
            CommonRepository.delete_object_from_db(subcategory)
            return {"message": "subcategory successfully deleted"}, 200

        return {"message": "subcategory with such id doesn't exist"}, 404
