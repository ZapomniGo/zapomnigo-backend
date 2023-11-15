from datetime import datetime, timedelta
from os import getenv

import jwt

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD, DevConfig, IS_OFFLINE, ProdConfig
from src.database.models import Users


def create_access_jwt_token(user: Users, raw_password: str) -> str:
    if ADMIN_EMAIL == user.email and ADMIN_PASSWORD == raw_password:

        payload = {"sub": user.user_id,
                   "name": f"{user.name}", "admin": True,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    else:
        payload = {"sub": user.user_id,
                   "name": f"{user.name}", "admin": False,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    if IS_OFFLINE:
        token = jwt.encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
    else:
        token = jwt.encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

    return token


def create_refresh_jwt_token(user: Users) -> str:
    payload = {"sub": user.user_id,
               "exp": datetime.utcnow() + timedelta(days=30)}

    if IS_OFFLINE:
        token = jwt.encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
    else:
        token = jwt.encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

    return token
