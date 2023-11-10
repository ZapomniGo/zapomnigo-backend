from src.database.models import SubscriptionModels
from src.database.models.base import db


class SubscriptionModelsRepository:
    @staticmethod
    def get_subscription_model_id(subscription_model: str) -> str:
        subscription_model = db.session.query(SubscriptionModels).filter_by(
            subscription_model=subscription_model).first()

        return subscription_model.subscription_model_id
