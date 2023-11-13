from typing import Tuple, Dict, Any

from flask import Blueprint

from src.controllers import UsersController as c

users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
def register() -> Tuple[Dict[str, Any], int]:
    return c.register_user()


@users_bp.post("/login")
def login() -> Tuple[Dict[str, Any], int]:
    return c.login_user()
