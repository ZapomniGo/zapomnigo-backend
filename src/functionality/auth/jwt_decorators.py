from functools import wraps

import jwt
from flask import request

from src.config import SECRET_KEY


def admin_required(f):
    @wraps(f)
    def admin_token_check(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        if access_token:

            decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            if decoded_token.get("admin"):
                return f(*args, **kwargs)

            else:
                return {"message": "Admin privileges required."}, 403
        else:
            return {"message": "Invalid or missing auth token."}, 499

    return admin_token_check


def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('Authorization')

        if access_token:
            jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            return f(*args, **kwargs)

        else:
            return {"message": "Invalid or missing auth token."}, 499

    return wrapper
