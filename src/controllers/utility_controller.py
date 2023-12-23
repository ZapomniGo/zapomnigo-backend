from typing import Tuple, Dict, Any

from flask import request
from jwt import decode

from src.config import SECRET_KEY, ADMIN_USERNAME


class UtilityController:

    @staticmethod
    def get_health() -> Tuple[Dict[str, str], int]:
        return {"status": "healthy"}, 200

    @classmethod
    def check_user_access(cls, username: str) -> Tuple[Dict[str, Any], int] | None:
        """Returns a JSON Response if there is an error or the user doesn't have access"""
        logged_in_username = cls.get_session_username()
        if not logged_in_username:
            return {"message": "No username provided"}, 400

        if logged_in_username == ADMIN_USERNAME or logged_in_username == username:
            return None

        return {"message": "Admin privileges required."}, 403

    @classmethod
    def get_session_username(cls) -> str | None:
        return decode(request.cookies.get('refresh_token'), SECRET_KEY, algorithms=["HS256"]).get("username")
