from typing import Tuple, Any, Dict

from flask import Blueprint

from src.auth.jwt_decorators import jwt_required
from src.controllers.folders_controller import FoldersController as c

folders_bp = Blueprint("folders", __name__)


@folders_bp.post("/folders")
@jwt_required
def create_folder() -> Tuple[Dict[str, Any], int]:
    return c.add_folder()
