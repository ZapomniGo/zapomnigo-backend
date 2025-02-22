from typing import Tuple, Dict, Any

from flask import Blueprint

from src.controllers.sets_controller import SetsController as c
from src.functionality.auth.jwt_decorators import jwt_required, admin_required
from src.limiter import limiter

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


@sets_bp.post("/sets/<set_id>/study")
@jwt_required
def create_studied_set(set_id: str):
    return c.create_studied_set(set_id)


@sets_bp.post("/sets/<set_id>/report")
@jwt_required
@limiter.limit("60/hour")
def report_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.report_set(set_id)


@sets_bp.post("/sets/<set_id>/verify")
@admin_required
def change_verified_status_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.change_verified_status_set(set_id)


@sets_bp.post("/sets/<set_id>/folders/<folder_id>")
@jwt_required
def add_set_to_folder(set_id: str, folder_id: str) -> Tuple[Dict[str, Any], int]:
    return c.add_set_to_folder(set_id, folder_id)
