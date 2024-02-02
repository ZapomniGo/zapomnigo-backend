from flask import Blueprint

from src.controllers.subcategories_controller import SubcategoriesController as c
from src.functionality.auth.jwt_decorators import admin_required

subcategories_bp = Blueprint("subcategories", __name__)


@subcategories_bp.post("/subcategories")
@admin_required
def create_subcategory():
    return c.add_subcategory()


@subcategories_bp.post("/categories/<category_id>/subcategories")
@admin_required
def create_subcategories_for_category(category_id: str):
    return c.create_subcategories_for_category(category_id)


@subcategories_bp.get("/categories/<category_id>/subcategories")
def get_subcategories_for_category(category_id: str):
    return c.get_subcategories_for_category(category_id)
