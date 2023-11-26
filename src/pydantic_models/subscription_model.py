from typing import Literal

from pydantic import BaseModel

SUBSCRIPTION_MODELS = Literal["6 months", "1 month", "1 year", "Free trial"]


class SubscriptionModel(BaseModel):
    subscription_model: SUBSCRIPTION_MODELS
