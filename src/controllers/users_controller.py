import asyncio
from typing import Tuple, Dict, Any

from flask import request, make_response, Response
from flask_bcrypt import generate_password_hash, check_password_hash
from jwt import decode
from ulid import ULID

from src.auth.jwt_creation import JwtCreation
from src.config import SECRET_KEY
from src.controllers.utility_controller import UtilityController
from src.controllers.verification_controller import VerificationController
from src.database.models import Users, OrganizationsUsers
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.organizations_repository import OrganizationsRepository
from src.database.repositories.users_repository import UsersRepository
from src.pydantic_models import RegistrationModel, LoginModel
from src.pydantic_models.reset_password_model import ResetPasswordModel
from src.services.mailer import send_email_background_task
from src.utilities.parsers import validate_json_body


class UsersController:

    @staticmethod
    def create_user(json_data) -> Users:
        hashed_password = generate_password_hash(json_data["password"]).decode("utf-8")

        return Users(user_id=str(ULID()), username=json_data["username"],  # type: ignore
                     name=json_data["name"], email=json_data["email"],
                     password=hashed_password, age=json_data.get("age", None),
                     gender=json_data.get("gender", None),  # type: ignore
                     privacy_policy=json_data["privacy_policy"],
                     terms_and_conditions=json_data["terms_and_conditions"],
                     marketing_consent=json_data["marketing_consent"])

    @classmethod
    async def register_user(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        validation_errors = validate_json_body(json_data, RegistrationModel)  # type: ignore
        if validation_errors:
            return {"validation errors": validation_errors}, 422

        user = cls.create_user(json_data)
        CommonRepository.add_object_to_db(user)

        if organization_id := json_data.get("organization", None):

                obj = OrganizationsUsers(organization_user_id=str(ULID()),
                                         user_id=user.user_id, organization_id=str(organization_id))
                CommonRepository.add_object_to_db(obj)

        await UtilityController.send_mail_logic(user.email, user.username)
        return {"message": "user added to db"}, 200

    @classmethod
    def login_user(cls) -> Response | Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        validation_errors = validate_json_body(json_data, LoginModel)  # type: ignore
        if validation_errors:
            return {"validation errors": validation_errors}, 422

        user = cls.check_if_user_exists(json_data)
        if not user:
            return {"message": "user doesn't exist"}, 404

        hashed_user_password = user.password
        if not check_password_hash(hashed_user_password, json_data["password"]):
            return {"message": "invalid password"}, 401

        if not user.verified:
            return {"user_info": {"email": user.email,
                                  "user_id": user.user_id,
                                  "username": user.username}}, 418

        access_token = JwtCreation.create_access_jwt_token(user=user, password=json_data["password"])
        refresh_token = JwtCreation.create_refresh_jwt_token(user.username)

        response = make_response({"message": "user logged in"}, 200)
        response.set_cookie('access_token', access_token, secure=True,
                            samesite="None", domain="localhost")
        response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite="None",domain="localhost")
        return response

    @classmethod
    def logout(cls) -> Response:
        response = make_response({"message": "user logged out"}, 200)
        response.set_cookie('access_token', '', expires=0, secure=True, samesite="None")
        response.set_cookie('refresh_token', '', expires=0, httponly=True, secure=True, samesite="None")
        return response

    @classmethod
    def refresh_token(cls) -> Response:
        refresh_token = request.cookies.get('refresh_token')
        decoded_token = decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

        # TODO: Implement Refresh Token Reuse Detection with Redis

        new_access_token = JwtCreation.create_access_jwt_token(username=decoded_token.get("username"), refresh=True)
        new_refresh_token = JwtCreation.create_refresh_jwt_token(decoded_token.get("username"))

        response = make_response({'message': 'Token refreshed'}, 200)
        response.set_cookie('access_token', new_access_token, secure=True, samesite="None")
        response.set_cookie('refresh_token', new_refresh_token, httponly=True, secure=True, samesite="None")

        return response

    @classmethod
    def reset_password(cls, json_data) -> Tuple[Dict[str, Any], int]:
        validation_errors = validate_json_body(json_data, ResetPasswordModel)
        if validation_errors:
            return {"validation errors": validation_errors}, 422

        response, status_code = VerificationController.verify_token(json_data["token"], is_verification=False)

        if status_code != 200:
            return response, status_code

        user = UsersRepository.get_user_by_username(response.get("username"))
        if not user:
            return {"message": "user doesn't exist"}, 404

        UsersRepository.reset_password(user, json_data["new_password"])
        return {"message": "Your password has been changed"}, 200
    @classmethod
    def check_if_user_exists(cls, json_data) -> Users | None:
        email_or_username = json_data["email_or_username"]

        if user := UsersRepository.get_user_by_username(email_or_username):
            return user

        elif user := UsersRepository.get_user_by_email(email_or_username):
            return user

        return None
