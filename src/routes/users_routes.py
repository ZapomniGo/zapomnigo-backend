from typing import Tuple, Dict

from flask import Blueprint

from src.controllers import UsersController as c

users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
def register() -> Tuple[Dict[str, str], int]:
    return c.register_user()
