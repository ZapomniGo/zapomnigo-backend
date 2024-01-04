from typing import Tuple, Dict, Any

from flask import Blueprint, Response, request

from src.controllers.users_controller import UsersController as c
from src.pydantic_models.reset_password_model import ResetPasswordModel
from src.utilities.parsers import validate_json_body

users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
async def register() -> Tuple[Dict[str, Any], int]:
    return await c.register_user()


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
    json_data = request.get_json()

    validation_errors = validate_json_body(json_data, ResetPasswordModel)
    if validation_errors:
        return {"validation errors": validation_errors}, 422

    return c.reset_password(json_data)