from src.database.models import Organizations
from src.database.models.base import db


class OrganizationsRepository:
    @classmethod
    def get_organization_by_id(cls, organization_id: str) -> Organizations | None:
        return db.session.query(Organizations).filter_by(organization_id=organization_id).first()

    @classmethod
    def get_organization_name_by_id(cls, organization_id: str) -> str | None:
        if organization := cls.get_organization_by_id(organization_id):
            return organization.organization_name

        return None
