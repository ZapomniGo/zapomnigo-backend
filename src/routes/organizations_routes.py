from typing import Tuple, Dict, Any

from flask import Blueprint
from src.controllers import OrganizationsController as c

organizations_bp = Blueprint("organizations", __name__)


@organizations_bp.get("/organizations")
def get_organizations() -> Tuple[Dict[str, Any], int]:
    return c.get_all_organizations()


@organizations_bp.get("/organizations/<organization_id>")
def get_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_organization(organization_id)
