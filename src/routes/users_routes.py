from typing import Tuple, Dict, Any

from celery.result import AsyncResult
from flask import Blueprint, Response, jsonify

from src.controllers.users_controller import UsersController as c
from src.controllers.utility_controller import UtilityController
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.jwt_decorators import jwt_required
from src.limiter import limiter

users_bp = Blueprint("users", __name__)


@users_bp.post("/register")
def register() -> Tuple[Dict[str, Any], int]:
    return c.register_user()


@users_bp.post("/login")
def login() -> Response | Tuple[Dict[str, Any], int]:
    return c.login_user()


@users_bp.post("/logout")
def logout() -> Response:
    return c.logout()


@users_bp.post("/refresh")
def refresh():
    return c.refresh_token()


@users_bp.post("/forgot-password")
def reset_password_route():
    return c.reset_password()


@users_bp.put("/users/<user_id>")
@jwt_required
def edit_user(user_id: str):
    return c.edit_user(user_id)


@users_bp.delete("/users/<user_id>")
@jwt_required
def delete_user(user_id: str):
    return c.delete_user(user_id)


@users_bp.get("/users/<user_id>")
@jwt_required
@limiter.limit("1/week")
def export_user_data(user_id: str):
    return c.export_user_data(user_id)


# https://flask.palletsprojects.com/en/2.3.x/patterns/celery/#getting-results
@users_bp.get("/users/<user_id>/tasks/<task_id>")
@jwt_required
def get_task_status(user_id: str, task_id: str):
    user = UsersRepository.get_user_by_ulid(user_id)
    if not user:
        return {"message": "user doesn't exist"}, 404

    if result := UtilityController.check_user_access(user.username):
        return result

    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Task is pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'result': task.result,
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info)
        }

    return jsonify(response)
