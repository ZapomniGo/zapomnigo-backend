from typing import Tuple, Dict, Any

from quart import Blueprint, request

from src.auth.jwt_decorators import admin_required
from src.controllers.organization_controller import OrganizationsController as c

organizations_bp = Blueprint("organizations", __name__)


@organizations_bp.get("/organizations")
async def get_organizations() -> Tuple[Dict[str, Any], int]:
    return c.get_all_organizations()


@organizations_bp.get("/organizations/<organization_id>")
@admin_required
async def get_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_organization(organization_id)


@organizations_bp.get("/organizations/<organization_id>/sets")
@admin_required
async def get_sets_for_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_sets_for_organization(organization_id)


@organizations_bp.post("/organizations")
@admin_required
async def register_organization() -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.add_organization(json_data)


@organizations_bp.delete("/organizations/<organization_id>")
@admin_required
async def delete_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_organization(organization_id)


@organizations_bp.put("/organizations/<organization_id>")
@admin_required
async def update_organization(organization_id: str) -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.update_organization(organization_id, json_data)
