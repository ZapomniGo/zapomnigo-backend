from typing import Tuple, Dict, Any

from flask import Blueprint
from quart import request

from src.auth.jwt_decorators import admin_required
from src.controllers.subscription_models_controller import SubscriptionModelsController as c

subscription_models_bp = Blueprint("subscription_models", __name__)


@subscription_models_bp.post("/subscription-models")
@admin_required
async def create_subscription_models_route() -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.add_subscription_model(json_data)
