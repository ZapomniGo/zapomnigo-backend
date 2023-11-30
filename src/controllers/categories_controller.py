from typing import Tuple, Any, Dict

from flask import request
from ulid import ULID

from src.database.models import Categories
from src.database.repositories import CommonRepository
from src.pydantic_models.categories_model import CategoriesModel
from src.utilities.parsers import validate_json_body


class CategoriesController:

    @classmethod
    def create_category(cls, json_data):
        return Categories(category_id=str(ULID()), category_name=str(json_data["category_name"]).lower())

    @classmethod
    def add_category(cls):
        json_data = request.json

        if validation_errors := validate_json_body(json_data, CategoriesModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_category(json_data))

        return {"message": "Category added to db"}, 200

    @classmethod
    def get_all_categories(cls) -> Tuple[Dict[str, Any], int]:
        if result := CommonRepository.get_all_objects_from_db(Categories):
            return {"categories": [categories.to_json() for categories in result]}, 200

        return {"message": "No categories were found"}, 404

    # @classmethod
    # def get_organization(cls, organization_id: str) -> Tuple[Dict[str, Any], int]:
    #     if organization := OrganizationsRepository.get_organization_by_id(organization_id):
    #         return {"organization": organization.to_json()}, 200
    #
    #     return {"message": "Organization with such id doesn't exist"}, 404
