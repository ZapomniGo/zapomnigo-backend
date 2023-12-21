from typing import Dict, Any

from src.database.models import Categories
from src.database.models.base import db


class CategoriesRepository:
    @classmethod
    def get_category_by_id(cls, category_id: str) -> Categories | None:
        return db.session.query(Categories).filter_by(category_id=category_id).first()

    @classmethod
    def edit_category(cls, category: Categories, json_data: Dict[str, Any]) -> None:
        category.category_name = json_data.get("category_name", category.category_name).lower()
        db.session.commit()
