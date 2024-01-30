from src.database.models import Categories, Subcategories
from src.database.models.base import db


class CategoriesRepository:
    @classmethod
    def get_category_by_id(cls, category_id: str) -> Categories | None:
        return db.session.query(Categories).filter_by(category_id=category_id).first()

    @classmethod
    def get_all_subcategories_by_category_id(cls, category_id: str) -> list[Subcategories] | None:
        return db.session.query(Subcategories).filter_by(category_id=category_id).all()

    @classmethod
    def get_subcategory_by_id(cls, subcategory_id: str) -> Subcategories | None:
        return db.session.query(Subcategories).filter_by(subcategory_id=subcategory_id).first()

    @classmethod
    def get_category_name_by_id(cls, category_id: str) -> str | None:
        if category := cls.get_category_by_id(category_id):
            return category.category_name

        return None

    @classmethod
    def get_subcategory_name_by_id(cls, subcategory_id: str) -> str | None:
        if subcategory := cls.get_subcategory_by_id(subcategory_id):
            return subcategory.subcategory_name

        return None
