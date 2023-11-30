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
