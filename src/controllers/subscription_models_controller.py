from typing import Tuple, Dict, Any

from flask import request
from ulid import ULID

from src.database.models import SubscriptionModels
from src.database.repositories.common_repository import CommonRepository
from src.pydantic_models.subscription_model import SubscriptionModel
from src.utilities.parsers import validate_json_body


class SubscriptionModelsController:

    @classmethod
    def create_subscription_model(cls, json_data) -> SubscriptionModels:
        return SubscriptionModels(subscription_model_id=str(ULID()),  # type: ignore
                                  subscription_model=json_data["subscription_model"])

    @classmethod
    def add_subscription_model(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, SubscriptionModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_subscription_model(json_data))

        return {"message": "subscription model added to db"}, 200
