from typing import Tuple, Dict, Any

from flask import Blueprint
from src.controllers import SubscriptionModelsController as c

subscription_models_bp = Blueprint("subscription_models", __name__)


@subscription_models_bp.post("/subscription-models")
def create_subscription_models_route() -> Tuple[Dict[str, Any], int]:
    return c.add_subscription_model()
