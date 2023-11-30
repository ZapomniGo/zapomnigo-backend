from flask import Blueprint
from src.controllers.categories_controller import CategoriesController as c

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("/categories")
def get_categories():
    pass


@categories_bp.get("/categories/<category_id>")
def get_category():
    pass


@categories_bp.post("/categories")
def create_category():
    return c.add_category()


@categories_bp.put("/categories/<category_id>")
def edit_category():
    pass


@categories_bp.delete("/categories/<category_id>")
def delete_category():
    pass
