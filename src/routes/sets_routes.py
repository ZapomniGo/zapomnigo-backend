from typing import Tuple, Dict, Any

from flask import Blueprint

from src.auth.jwt_decorators import admin_required, jwt_required
from src.controllers.sets_controller import SetsController as c

sets_bp = Blueprint("sets", __name__)


@sets_bp.get("/sets")
def get_sets() -> Tuple[Dict[str, Any], int]:
    return c.get_all_sets()


@sets_bp.get("/sets/<set_id>")
def get_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_set(set_id)


@sets_bp.post("/sets")
@jwt_required
def create_set() -> Tuple[Dict[str, Any], int]:
    return c.add_set()


@sets_bp.delete("/sets/<set_id>")
@jwt_required
def delete_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_set(set_id)


@sets_bp.put("/sets/<set_id>")
@jwt_required
def update_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.update_set(set_id)


@sets_bp.get("/users/<user_id>/sets")
@jwt_required
def get_sets_for_user(user_id: str):
    return c.get_sets_for_user(user_id)

@sets_bp.post("/sets/<set_id>/copy")
@jwt_required
def copy_set(set_id: str):
    return c.copy_set(set_id)

@sets_bp.get("/sets/<set_id>/study")
@jwt_required
def study_set(set_id: str):
    return c.study_set(set_id)