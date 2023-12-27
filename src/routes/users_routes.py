from typing import Tuple, Dict, Any

from flask import Blueprint, Response
from quart import request

from src.controllers.users_controller import UsersController as c

users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
async def register() -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.register_user(json_data)


@users_bp.post("/login")
async def login() -> Response | Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return await c.login_user(json_data)


@users_bp.post("/logout")
async def logout() -> Response:
    return await c.logout()


@users_bp.post("/refresh")
async def refresh():
    return await c.refresh_token()
