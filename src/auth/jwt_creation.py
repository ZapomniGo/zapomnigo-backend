from datetime import datetime, timedelta

import jwt
from flask_bcrypt import check_password_hash

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD, DevConfig, IS_OFFLINE, ProdConfig, SECRET_KEY, ADMIN_USERNAME
from src.database.models import Users
from src.database.repositories.users_repository import UsersRepository


class JwtCreation:

    @classmethod
    def create_access_jwt_token(cls, username: str) -> str:
        if username == ADMIN_USERNAME:
            is_admin = True
        else:
            is_admin = False

        payload = {
            "username": username,
            "admin": is_admin,
            "exp": datetime.utcnow() + timedelta(hours=12)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    def create_refresh_jwt_token(cls, username: str) -> str:
        payload = {"username": username,
                   "exp": datetime.utcnow() + timedelta(days=30)}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return token
