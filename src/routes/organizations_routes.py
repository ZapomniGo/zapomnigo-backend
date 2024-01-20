from typing import Tuple, Dict, Any

from flask import Blueprint

from src.controllers.organization_controller import OrganizationsController as c
from src.functionality.auth.jwt_decorators import admin_required

organizations_bp = Blueprint("organizations", __name__)


@organizations_bp.get("/organizations")
def get_organizations() -> Tuple[Dict[str, Any], int]:
    return c.get_all_organizations()


@organizations_bp.get("/organizations/<organization_id>")
@admin_required
def get_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_organization(organization_id)


@organizations_bp.get("/organizations/<organization_id>/sets")
@admin_required
def get_sets_for_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_sets_for_organization(organization_id)


@organizations_bp.post("/organizations")
@admin_required
def register_organization() -> Tuple[Dict[str, Any], int]:
    return c.add_organization()


@organizations_bp.delete("/organizations/<organization_id>")
@admin_required
def delete_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_organization(organization_id)


@organizations_bp.put("/organizations/<organization_id>")
@admin_required
def update_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.update_organization(organization_id)
