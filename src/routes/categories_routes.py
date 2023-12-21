from flask import Blueprint

from src.auth.jwt_decorators import admin_required
from src.controllers.categories_controller import CategoriesController as c

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("/categories")
def get_categories():
    return c.get_all_categories()


@categories_bp.get("/categories/<category_id>")
def get_category(category_id: str):
    return c.get_category(category_id)


@categories_bp.post("/categories")
# @admin_required
def create_category():
    return c.add_category()


@categories_bp.put("/categories/<category_id>")
def edit_category():
    pass


@categories_bp.delete("/categories/<category_id>")
def delete_category(category_id: str):
    return c.delete_category(category_id)
