from datetime import datetime, timedelta

import jwt

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD, DevConfig, IS_OFFLINE, ProdConfig, SECRET_KEY
from src.database.models import Users


def create_access_jwt_token(**kwargs) -> str:
    user: Users = kwargs.get("user")
    raw_password: str = kwargs.get("password")
    sub: str = kwargs.get("sub")

    if user:
        sub = user.user_id

    if ADMIN_EMAIL == user.email and ADMIN_PASSWORD == raw_password:

        payload = {"sub": sub, "admin": True,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    else:
        payload = {"sub": sub, "admin": False,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return token


def create_refresh_jwt_token(user_id: str) -> str:
    payload = {"sub": user_id,
               "exp": datetime.utcnow() + timedelta(days=30)}

    if IS_OFFLINE:
        token = jwt.encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
    else:
        token = jwt.encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

    return token
