from typing import Tuple, Any, Dict

from flask import Blueprint

from src.auth.jwt_decorators import jwt_required
from src.controllers.folders_controller import FoldersController as c

folders_bp = Blueprint("folders", __name__)


@folders_bp.post("/folders")
@jwt_required
def create_folder() -> Tuple[Dict[str, Any], int]:
    return c.add_folder()


@folders_bp.delete("/folders/<folder_id>")
@jwt_required
def delete_folder(folder_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_folder(folder_id)


@folders_bp.put("/folders/<folder_id>")
@jwt_required
def edit_folder(folder_id: str) -> Tuple[Dict[str, Any], int]:
    return c.edit_folder(folder_id)


@folders_bp.get("/folders/<folder_id>/sets")
def get_sets_for_folder(folder_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_all_sets_in_folder(folder_id)


@folders_bp.get("users/<user_id>/folders")
def get_all_folders_for_user(user_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_all_folders_for_user(user_id)
