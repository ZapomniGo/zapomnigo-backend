from typing import Dict, Any

from src.database.models import Categories
from src.database.models.base import db
from src.pydantic_models.categories_model import CategoriesModel
from src.utilities.parsers import filter_none_values


class CategoriesRepository:
    @classmethod
    def get_category_by_id(cls, category_id: str) -> Categories | None:
        return db.session.query(Categories).filter_by(category_id=category_id).first()

    @classmethod
    def get_category_name_by_id(cls, category_id: str) -> str | None:
        if category := cls.get_category_by_id(category_id):
            return category.category_name

        return None

    @classmethod
    def edit_category(cls, category: Categories, json_data: CategoriesModel) -> None:
        for field_name, value in filter_none_values(json_data).items():
            setattr(category, field_name, value)

        db.session.commit()
