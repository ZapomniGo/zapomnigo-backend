from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.pydantic_models.common import NAME
from src.pydantic_models.subscription_model import SUBSCRIPTION_MODELS


class OrganizationModel(BaseModel):
    organization_name: NAME
    organization_domain: str
    subscription_model: SUBSCRIPTION_MODELS


class UpdateOrganizationModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    organization_name: Optional[NAME] = None
    organization_domain: Optional[str] = None
    subscription_model: Optional[SUBSCRIPTION_MODELS] = None
