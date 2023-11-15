from datetime import datetime, timedelta
from os import getenv

import jwt

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD
from src.database.models import Users


def create_access_jwt_token(user: Users, raw_password: str) -> str:
    if ADMIN_EMAIL == user.email and ADMIN_PASSWORD == raw_password:

        payload = {"sub": user.id,
                   "name": f"{user.name}", "admin": True,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    else:
        payload = {"sub": user.user_id,
                   "name": f"{user.name}", "admin": False,
                   "exp": datetime.utcnow() + timedelta(hours=1)}

    token = jwt.encode(payload, getenv("SECRET_KEY"), algorithm="HS256")

    return token


def create_refresh_jwt_token(user: Users) -> str:
    payload = {"sub": user.id,
               "exp": datetime.utcnow() + timedelta(days=30)}
    token = jwt.encode(payload, getenv("SECRET_KEY"), algorithm="HS256")

    return token
