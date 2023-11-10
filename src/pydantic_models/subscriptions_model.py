from typing import Literal

from pydantic import BaseModel


class SubscriptionModel(BaseModel):
    subscription_models: Literal["6 months", "1 month", "1 year"]