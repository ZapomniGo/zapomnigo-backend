from typing import Tuple, Dict

from flask import Blueprint
from src.controllers.utility_controller import UtilityController as c

utility_bp = Blueprint("utility", __name__)


@utility_bp.get("/health")
def health() -> Tuple[Dict[str, str], int]:
    return c.get_health()


@utility_bp.get("/search")
def search() -> Tuple[Dict[str, str], int]:
    return c.search()
