from typing import Tuple, Dict, Any

from flask import request
from ulid import ULID

from src.database.models import Organizations
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.organizations_repository import OrganizationsRepository
from src.database.repositories.subscription_models_repository import SubscriptionModelsRepository
from src.pydantic_models.organization_model import OrganizationModel, UpdateOrganizationModel
from src.utilities.parsers import validate_json_body


class OrganizationsController:
    @classmethod
    def get_all_organizations(cls) -> Tuple[Dict[str, Any], int]:
        if result := CommonRepository.get_all_objects_from_db(Organizations):
            return {"organizations": [organization.public_to_json() for organization in result]}, 200

        return {"message": "No organizations were found"}, 404

    @classmethod
    def get_organization(cls, organization_id: str) -> Tuple[Dict[str, Any], int]:
        if organization := OrganizationsRepository.get_organization_by_id(organization_id):
            return {"organization": organization.to_json()}, 200

        return {"message": "Organization with such id doesn't exist"}, 404

    @staticmethod
    def create_organization(json_data):
        subscription_model_id = SubscriptionModelsRepository.get_subscription_model_id(json_data["subscription_model"])

        return Organizations(organization_id=str(ULID()), organization_name=json_data["organization_name"],
                             organization_domain=json_data["organization_domain"],
                             subscription_model_id=subscription_model_id)

    @classmethod
    def add_organization(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()
        if validation_errors := validate_json_body(json_data, OrganizationModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_organization(json_data))

        return {"message": "Organization added to db"}, 200

    @classmethod
    def delete_organization(cls, organization_id: str) -> Tuple[Dict[str, Any], int]:
        if organization := OrganizationsRepository.get_organization_by_id(organization_id):
            CommonRepository.delete_object_from_db(organization)
            return {"message": "Organization successfully deleted"}, 200

        return {"message": "Organization with such id doesn't exist"}, 404

    @classmethod
    def update_organization(cls, organization_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()
        organization = OrganizationsRepository.get_organization_by_id(organization_id)

        if not organization:
            return {"message": "Organization with such id doesn't exist"}, 404

        if validation_errors := validate_json_body(json_data, UpdateOrganizationModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        OrganizationsRepository.edit_organization(organization, json_data)
        return {"message": "Organization successfully updated"}, 200
