from flask import Blueprint

from src.controllers.categories_controller import CategoriesController as c
from src.functionality.auth.jwt_decorators import jwt_required, admin_required

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("/categories")
def get_categories():
    return c.get_all_categories()


@categories_bp.get("/categories/<category_id>")
def get_category(category_id: str):
    return c.get_category(category_id)


@categories_bp.post("/categories")
@jwt_required
def create_category():
    return c.add_category()


@categories_bp.put("/categories/<category_id>")
@admin_required
def edit_category(category_id: str):
    return c.update_category(category_id)


@categories_bp.delete("/categories/<category_id>")
@admin_required
def delete_category(category_id: str):
    return c.delete_category(category_id)
