from sqlalchemy import asc

from src.database.models import Categories, Subcategories, CategorySubcategories
from src.database.models.base import db


class CategoriesRepository:
    @classmethod
    def get_category_by_id(cls, category_id: str) -> Categories | None:
        return db.session.query(Categories).filter_by(category_id=category_id).first()

    @classmethod
    def get_all_categories(cls) -> list[Categories] | None:
        return db.session.query(Categories).order_by(asc(Categories.order)).all()

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

    @classmethod
    def get_subcategories_for_category(cls, category_id):
        return db.session.query(Subcategories.subcategory_id, Subcategories.subcategory_name).join(
            CategorySubcategories, CategorySubcategories.subcategory_id == Subcategories.subcategory_id).filter_by(
            category_id=category_id).order_by(asc(CategorySubcategories.order)).all()
