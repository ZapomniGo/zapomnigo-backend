from quart import Blueprint, request

from src.auth.jwt_decorators import admin_required, jwt_required
from src.controllers.categories_controller import CategoriesController as c

categories_bp = Blueprint("categories", __name__)


@categories_bp.get("/categories")
async def get_categories():
    return c.get_all_categories()


@categories_bp.get("/categories/<category_id>")
async def get_category(category_id: str):
    return c.get_category(category_id)


@categories_bp.post("/categories")
@jwt_required
async def create_category():
    json_data = await request.get_json()
    return c.add_category(json_data)


@categories_bp.put("/categories/<category_id>")
@admin_required
async def edit_category(category_id: str):
    json_data = await request.get_json()
    return c.update_category(category_id, json_data)


@categories_bp.delete("/categories/<category_id>")
@admin_required
async def delete_category(category_id: str):
    return c.delete_category(category_id)
