from typing import Tuple, Dict, Any

from flask import Blueprint, Response

from src.controllers.users_controller import UsersController as c

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
