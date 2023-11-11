from typing import Tuple, Dict

from flask import Blueprint
from src.controllers import UtilityController as c

utility_bp = Blueprint("utility", __name__)


@utility_bp.get("/health")
def health() -> Tuple[Dict[str, str], int]:
    return c.get_health()
