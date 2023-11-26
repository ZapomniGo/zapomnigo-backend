from typing import Tuple, Dict, Any

from flask import request
from ulid import ULID

from src.database.models import Organizations
from src.database.repositories import OrganizationsRepository, SubscriptionModelsRepository
from src.database.repositories.common_repository import CommonRepository
from src.pydantic_models.organization_model import OrganizationModel
from src.utilities.parsers import validate_json_body


class OrganizationsController:
    @classmethod
    def get_all_organizations(cls) -> Tuple[Dict[str, Any], int]:
        if result := CommonRepository.get_all_objects_from_db(Organizations):
            return {"organizations": [organization.to_json() for organization in result]}, 200

        return {"message": "No organizations were found"}, 404

    @classmethod
    def get_organization(cls, organization_id: str) -> Tuple[Dict[str, Any], int]:
        if organization := OrganizationsRepository.get_organization_by_id(organization_id):
            return {"organization": organization.to_json()}, 200

        return {"message": "organization with such id doesn't exist"}, 404

    @staticmethod
    def create_organization(json_data):
        subscription_model_id = SubscriptionModelsRepository.get_subscription_model_id(json_data["subscription_model"])

        return Organizations(organization_id=str(ULID()), organization_name=json_data["organization_name"],
                             organization_domain=json_data["organization_domain"],
                             subscription_model_id=subscription_model_id)

    @classmethod
    def add_organization(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()
        validation_errors = validate_json_body(json_data, OrganizationModel)  # type: ignore
        if validation_errors:
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_organization(json_data))

        return {"message": "organization added to db"}, 200

    @classmethod
    def delete_organization(cls, organization_id: str) -> Tuple[Dict[str, Any], int]:
        if organization := OrganizationsRepository.get_organization_by_id(organization_id):
            CommonRepository.delete_object_from_db(organization)
            return {"message": "organization successfully deleted"}, 200

        return {"message": "organization with such id doesn't exist"}, 404
