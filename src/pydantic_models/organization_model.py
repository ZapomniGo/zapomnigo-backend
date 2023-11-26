from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints


class OrganizationModel(BaseModel):
    organization_name: Annotated[str, StringConstraints(min_length=2, max_length=40)]  # type: ignore
    organization_domain: str
    subscription_model: Literal["6 months", "1 month", "1 year", "Free trial"]
