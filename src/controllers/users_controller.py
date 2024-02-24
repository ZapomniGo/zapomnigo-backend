from typing import Tuple, Dict, Any

from flask import request, make_response, Response
from flask_bcrypt import generate_password_hash, check_password_hash
from jwt import decode

from src.config import SECRET_KEY
from src.controllers.verification_controller import VerificationController
from src.database.database_transaction_handlers import handle_database_session_transaction_async, \
    handle_database_session_transaction
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.mailing_functionality import MailingFunctionality
from src.functionality.users_functionallity import UsersFunctionality
from src.pydantic_models.users_models import ResetPasswordModel, RegistrationModel, LoginModel, UpdateUser
from src.utilities.parsers import validate_json_body


class UsersController:

    @classmethod
    @handle_database_session_transaction_async
    async def register_user(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, RegistrationModel):
            return {"validation errors": validation_errors}, 422

        user = UsersFunctionality.create_user(RegistrationModel(**json_data))
        CommonRepository.add_object_to_db(user)

        await MailingFunctionality.send_verification_email(user.email, user.username)
        return {"message": "user added to db"}, 200

    @classmethod
    def login_user(cls) -> Response | Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, LoginModel):
            return {"validation errors": validation_errors}, 422

        user = UsersFunctionality.check_if_user_exists(json_data)
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
    @handle_database_session_transaction
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
    @handle_database_session_transaction_async
    async def edit_user(cls, user_id: str) -> Tuple[Dict[str, Any], int]:
        # As this is an async func we cannot use the jwt_required decorator
        username = AuthFunctionality.get_session_username_or_user_id(request)
        if not username:
            return {"message": "No auth token provided"}, 499

        user = UsersRepository.get_user_by_ulid(user_id)
        if not user:
            return {"message": "user doesn't exist"}, 404

        json_data = request.get_json()
        if validation_errors := validate_json_body(json_data, UpdateUser):
            return {"validation errors": validation_errors}, 422

        user_update_fields = UpdateUser(**json_data)

        if user_update_fields.new_password and user_update_fields.password:
            if not check_password_hash(user.password, user_update_fields.password):
                return {"message": "invalid password"}, 401

            user_update_fields.password = generate_password_hash(user_update_fields.new_password).decode("utf-8")

        else:
            # Remove the password field if order to prevent updating the password without
            # passing the new_password as well
            user_update_fields.password = None

        if user_update_fields.email is not None and user_update_fields.email != user.email:
            UsersRepository.change_verified_status(user, False)

        CommonRepository.edit_object(user, user_update_fields)
        await UsersFunctionality.send_emails(user, user_update_fields)

        return {"message": "user updated"}, 200
