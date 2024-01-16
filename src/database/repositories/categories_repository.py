from typing import Dict, Any

from src.database.models import Categories
from src.database.models.base import db


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
    def edit_category(cls, category: Categories, json_data: Dict[str, Any]) -> None:
        category.category_name = json_data.get("category_name", category.category_name).lower()
        db.session.commit()
