from typing import Tuple, Dict, Any

from flask import Blueprint, Response

from src.controllers.users_controller import UsersController as c
from src.functionality.auth.jwt_decorators import jwt_required
from src.limiter import limiter

users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
def register() -> Tuple[Dict[str, Any], int]:
    return c.register_user()


@users_bp.post("/login")
def login() -> Response | Tuple[Dict[str, Any], int]:
    return c.login_user()


@users_bp.post("/logout")
def logout() -> Response:
    return c.logout()


@users_bp.post("/refresh")
def refresh():
    return c.refresh_token()


@users_bp.post("/forgot-password")
def reset_password_route():
    return c.reset_password()


@users_bp.put("/users/<user_id>")
@jwt_required
def edit_user(user_id: str):
    return c.edit_user(user_id)


@users_bp.delete("/users/<user_id>")
@jwt_required
def delete_user(user_id: str):
    return c.delete_user(user_id)


@users_bp.get("/users/<user_id>")
@limiter.limit("1/7 days")
@jwt_required
def export_user_data(user_id: str):
    return c.export_user_data(user_id)


@users_bp.get("/users/<user_id>/data/<task_id>")
@jwt_required
def get_export_user_data_task_status(user_id: str, task_id: str):
    return c.get_export_user_data_task_status(user_id, task_id)
