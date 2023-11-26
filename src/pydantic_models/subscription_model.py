from typing import Literal

from pydantic import BaseModel


class SubscriptionModel(BaseModel):
    subscription_model: Literal["6 months", "1 month", "1 year", "Free trial"]
