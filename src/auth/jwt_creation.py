from datetime import datetime, timedelta

import jwt
from flask_bcrypt import check_password_hash

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD, DevConfig, IS_OFFLINE, ProdConfig, SECRET_KEY, ADMIN_USERNAME
from src.database.models import Users
from src.database.repositories.users_repository import UsersRepository


class JwtCreation:

    @classmethod
    def create_access_jwt_token(cls, **kwargs) -> str:
        user: Users = kwargs.get("user")
        raw_password = kwargs.get("password")
        username = kwargs.get("username")
        refresh = kwargs.get("refresh")

        if refresh:
            if username == ADMIN_USERNAME:
                is_admin = True
            else:
                is_admin = False
        else:
            if username:
                user = UsersRepository.get_user_by_username(username)
                is_admin = (user.email == ADMIN_EMAIL and check_password_hash(user.password, raw_password))
            else:
                is_admin = (user.email == ADMIN_EMAIL and check_password_hash(user.password, raw_password))
                username = user.username

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

        if IS_OFFLINE:
            token = jwt.encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
        else:
            token = jwt.encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    def create_verification_jwt(cls, user_id: str) -> str:
        payload = {"sub": user_id,
                   "exp": datetime.utcnow() + timedelta(hours=48)}

        if IS_OFFLINE:
            token = jwt.encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
        else:
            token = jwt.encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

        return token
