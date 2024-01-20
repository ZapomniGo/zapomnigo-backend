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
