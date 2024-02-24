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
from src.pydantic_models.users_models import ResetPasswordModel, RegistrationModel, LoginModel, UpdateUser
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
    async def edit_uer(cls, user_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, UpdateUser):
            return {"validation errors": validation_errors}, 422

        user = UsersRepository.get_user_by_ulid(user_id)
        if not user:
            return {"message": "user doesn't exist"}, 404

        user_update_fields = UpdateUser(**json_data)

        if user_update_fields.new_password and user_update_fields.password:
            error_message, status_code = await cls.update_password(user, user_update_fields)
            if error_message:
                return error_message, status_code

        else:
            # Remove the password field if order to prevent updating the password without
            # passing the new_password as well
            user_update_fields.password = None

        if user_update_fields.email:
            if user_update_fields.email != user.email:
                user_update_fields.verified = False
                await MailingFunctionality.send_verification_email(user_update_fields.email, user.username,
                                                                   verify_on_register=False)

        CommonRepository.edit_object(user, user_update_fields)

        return {"message": "user updated"}, 200

    @classmethod
    async def update_password(cls, user, user_update_fields):
        if not check_password_hash(user.password, user_update_fields.password):
            return {"message": "invalid password"}, 401

        hashed_password = generate_password_hash(user_update_fields.new_password).decode("utf-8")
        user_update_fields.password = hashed_password
        await MailingFunctionality.send_reset_password_email(user.email, user.username, is_change_password=True)

        return None, None
