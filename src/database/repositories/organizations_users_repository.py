from src.database.models import OrganizationsUsers, Organizations
from src.database.models.base import db


class OrganizationsUsersRepository:

    @classmethod
    def get_organization_by_user_id(cls, user_id: str) -> Organizations | None:
        if result := db.session.query(OrganizationsUsers).filter_by(user_id=user_id).first():
            return db.session.query(Organizations).filter_by(organization_id=result.organization_id).first()

        return None
