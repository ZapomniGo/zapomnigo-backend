from typing import Tuple, Dict, Any

from src.database.models import Organizations
from src.database.models.base import db
from src.database.repositories import OrganizationsRepository
from src.database.repositories.common_repository import CommonRepository


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
