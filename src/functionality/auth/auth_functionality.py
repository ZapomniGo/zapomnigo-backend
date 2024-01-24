from datetime import datetime, timedelta

import jwt
from flask import Request
from flask_bcrypt import check_password_hash
from jwt import decode, encode

from src.config import ADMIN_EMAIL, ADMIN_PASSWORD, DevConfig, IS_OFFLINE, \
    ProdConfig, SECRET_KEY, ADMIN_USERNAME
from src.database.models import Users
from src.database.repositories.organizations_users_repository import \
    OrganizationsUsersRepository
from src.database.repositories.users_repository import UsersRepository


class AuthFunctionality:

    @classmethod
    def create_access_jwt_token(cls, **kwargs) -> str:
        # These are passed on login
        user: Users = kwargs.get("user")
        raw_password = kwargs.get("password")

        # These are passed when refreshing jwt
        username = kwargs.get("username")
        refresh = kwargs.get("refresh")

        if refresh and username:
            if username == ADMIN_USERNAME:
                is_admin = True
            else:
                is_admin = False

            user = UsersRepository.get_user_by_username(username)
            user_id = user.user_id

        else:
            is_admin = (user.email == ADMIN_EMAIL and check_password_hash(
                user.password, raw_password))
            username = user.username
            user_id = user.user_id

        if organization := OrganizationsUsersRepository.get_organization_by_user_id(
                user_id):
            organization_name = organization.organization_name
        else:
            organization_name = None

        payload = {
            "sub": user_id,
            "username": username,
            "institution": organization_name,
            "admin": is_admin,
            "exp": datetime.utcnow() + timedelta(hours=12)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    def create_jwt_token(cls, username: str, is_refresh: bool = True) -> str:
        exp = datetime.utcnow() + timedelta(days=30)
        if not is_refresh:
            # This is for transactional emails
            exp = datetime.utcnow() + timedelta(hours=24)

        payload = {"username": username,
                   "exp": exp}

        if IS_OFFLINE:
            token = encode(payload, DevConfig.SECRET_KEY, algorithm="HS256")
        else:
            token = encode(payload, ProdConfig.SECRET_KEY, algorithm="HS256")

        return token

    @classmethod
    def get_session_username_or_user_id(cls, request: Request,
                                        get_username=True) -> str | None:
        access_token = request.headers.get('Authorization')
        if access_token:
            if get_username:
                return decode(access_token, SECRET_KEY,
                              algorithms=["HS256"]).get("username")
            else:
                return decode(access_token, SECRET_KEY,
                              algorithms=["HS256"]).get("sub")
        else:
            return None
