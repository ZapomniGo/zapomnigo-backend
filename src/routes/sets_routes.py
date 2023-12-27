from typing import Tuple, Dict, Any

from flask import Blueprint
from quart import request

from src.auth.jwt_decorators import jwt_required
from src.controllers.sets_controller import SetsController as c

sets_bp = Blueprint("sets", __name__)


@sets_bp.get("/sets")
async def get_sets() -> Tuple[Dict[str, Any], int]:
    return c.get_all_sets()


@sets_bp.get("/sets/<set_id>")
async def get_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_set(set_id)


@sets_bp.post("/sets")
@jwt_required
async def create_set() -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.add_set(json_data)

@sets_bp.delete("/sets/<set_id>")
@jwt_required
async def delete_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_set(set_id)


@sets_bp.put("/sets/<set_id>")
@jwt_required
async def update_set(set_id: str) -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.update_set(set_id, json_data)
