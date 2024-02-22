from typing import Tuple, Dict, Any

from flask import request, make_response, Response
from flask_bcrypt import generate_password_hash, check_password_hash
from jwt import decode
from ulid import ULID

from src.config import SECRET_KEY
from src.controllers.verification_controller import VerificationController
from src.database.models import Users, OrganizationsUsers
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.mailing_functionality import MailingFunctionality
from src.pydantic_models.users_models import ResetPasswordModel, RegistrationModel, LoginModel
from src.utilities.parsers import validate_json_body


class UsersController:

    @staticmethod
    def create_user(json_data: RegistrationModel) -> Users:
        hashed_password = generate_password_hash(json_data.password).decode("utf-8")

        return Users(user_id=str(ULID()), username=json_data.username,
                     name=json_data.name, email=json_data.email,
                     password=hashed_password, age=json_data.age,
                     gender=json_data.gender,
                     privacy_policy=json_data.privacy_policy,
                     terms_and_conditions=json_data.terms_and_conditions,
                     marketing_consent=json_data.marketing_consent)

    @classmethod
    async def register_user(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, RegistrationModel):
            return {"validation errors": validation_errors}, 422

        user = cls.create_user(RegistrationModel(**json_data))
        CommonRepository.add_object_to_db(user)

        # if organization_id := json_data.get("organization", None):
        #     obj = OrganizationsUsers(organization_user_id=str(ULID()),
        #                              user_id=user.user_id, organization_id=str(organization_id))
        #     CommonRepository.add_object_to_db(obj)

        await MailingFunctionality.send_mail_logic(user.email, user.username)
        return {"message": "user added to db"}, 200

    @classmethod
    def login_user(cls) -> Response | Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, LoginModel):
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

        access_token = AuthFunctionality.create_access_jwt_token(user=user, password=json_data["password"])
        refresh_token = AuthFunctionality.create_jwt_token(user.username)

        response = make_response(
            {"message": "user logged in", "access_token": access_token, "refresh_token": refresh_token}, 200)
        # response.set_cookie('access_token', access_token, secure=True, samesite="None", domain="localhost")
        # response.set_cookie('refresh_token', refresh_token, httponly=True, secure=True, samesite="None", domain="localhost")
        return response

    @classmethod
    def logout(cls) -> Response:
        response = make_response({"message": "user logged out"}, 200)
        # response.set_cookie('access_token', '', expires=0, secure=True, samesite="None", domain="localhost")
        # response.set_cookie('refresh_token', '', expires=0, httponly=True, secure=True, samesite="None", domain="localhost")
        return response

    @classmethod
    def refresh_token(cls) -> Response:
        refresh_token = request.headers.get('Authorization')
        decoded_token = decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

        # TODO: Implement Refresh Token Reuse Detection with Redis

        new_access_token = AuthFunctionality.create_access_jwt_token(username=decoded_token.get("username"),
                                                                     refresh=True)
        new_refresh_token = AuthFunctionality.create_jwt_token(decoded_token.get("username"))

        response = make_response(
            {'message': 'Token refreshed', 'access_token': new_access_token, "refresh_token": new_refresh_token}, 200)
        # response.set_cookie('access_token', new_access_token, secure=True, samesite="None", domain="localhost")
        # response.set_cookie('refresh_token', new_refresh_token, httponly=True, secure=True, samesite="None", domain="localhost")

        return response

    @classmethod
    def reset_password(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, ResetPasswordModel):
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

    @classmethod
    def edit_uer(cls, user_id: str, json_data: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        user = UsersRepository.get_user_by_ulid(user_id)
        if not user:
            return {"message": "user doesn't exist"}, 404

        UsersRepository.edit_user(user, json_data)
        return {"message": "user updated"}, 200