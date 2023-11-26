import jwt
from flask import request

from src.config import SECRET_KEY


def admin_required(f):
    def wrapper(*args, **kwargs):
        access_token = request.cookies.get("access_token")
        if access_token:

            decoded_token = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            if decoded_token.get("admin"):
                return f(*args, **kwargs)

            else:
                return {"Message": "Admin privileges required."}, 403
        else:
            return {"Message": "No auth token provided."}, 499

    return wrapper


def jwt_required(f):
    def wrapper(*args, **kwargs):
        access_token = request.cookies.get("access_token")

        if access_token:
            jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            return f(*args, **kwargs)

        else:
            return {"Message": "No auth token provided."}, 499

    return wrapper
