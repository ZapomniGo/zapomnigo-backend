from datetime import datetime, timedelta

import jwt
from flask_bcrypt import check_password_hash

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD, DevConfig, IS_OFFLINE, ProdConfig, SECRET_KEY
from src.database.repositories.users_repository import UsersRepository


class JwtCreation:

    @classmethod
    def create_access_jwt_token(cls, **kwargs) -> str:
        user = kwargs.get("user")
        raw_password = kwargs.get("password")
        sub = kwargs.get("sub")

        if sub:
            user = UsersRepository.get_user_by_ulid(sub)
            is_admin = (user.email == ADMIN_EMAIL and check_password_hash(user.password, ADMIN_PASSWORD))
        else:
            is_admin = (user.email == ADMIN_EMAIL and check_password_hash(user.password, raw_password))
            sub = user.user_id

        payload = {
            "sub": sub,
            "admin": is_admin,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    def create_refresh_jwt_token(cls, user_id: str) -> str:
        payload = {"sub": user_id,
                   "exp": datetime.utcnow() + timedelta(days=30)}

        if IS_OFFLINE:
            token = jwt.encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
        else:
            token = jwt.encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

        return token
