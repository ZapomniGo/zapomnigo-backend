from quart import Blueprint, current_app

from src.auth.jwt_decorators import admin_required, jwt_required
from src.controllers.categories_controller import CategoriesController as c
from src.services.mailer import send_mail_async

categories_bp = Blueprint("categories", __name__)


async def background_task():
    await send_mail_async("ivanobreshkov12@gmail.com", "Test", "Nasko e gei")


@categories_bp.get("/categories")
async def get_categories():
    current_app.add_background_task(background_task)
    return c.get_all_categories()


@categories_bp.get("/categories/<category_id>")
async def get_category(category_id: str):
    return c.get_category(category_id)


@categories_bp.post("/categories")
@jwt_required
async def create_category():
    return c.add_category()


@categories_bp.put("/categories/<category_id>")
@admin_required
async def edit_category(category_id: str):
    return c.update_category(category_id)


@categories_bp.delete("/categories/<category_id>")
@admin_required
async def delete_category(category_id: str):
    return c.delete_category(category_id)
