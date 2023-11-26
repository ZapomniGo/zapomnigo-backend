from typing import Dict, Any

from src.database.models import Organizations
from src.database.models.base import db
from src.database.repositories.subscription_models_repository import SubscriptionModelsRepository


class OrganizationsRepository:
    @classmethod
    def get_organization_by_id(cls, organization_id: str) -> Organizations | None:
        return db.session.query(Organizations).filter_by(organization_id=organization_id).first()

    @classmethod
    def edit_organization(cls, organization: Organizations, json_data: Dict[str, Any]) -> None:
        organization.organization_name = json_data.get("organization_name", organization.organization_name)
        organization.organization_domain = json_data.get("organization_domain", organization.organization_domain)
        if subscription_model_id := json_data.get("subscription_model", None):
            organization.subscription_model_id = SubscriptionModelsRepository.get_subscription_model_id(
                subscription_model_id)

        db.session.commit()
