import datetime
from typing import Tuple, Dict, Any

from flask import request
from flask_bcrypt import generate_password_hash, check_password_hash
from ulid import ULID

from src.database.models import Users
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.subscription_models_repository import SubscriptionModelsRepository
from src.database.repositories.users_repository import UsersRepository
from src.pydantic_models import RegistrationModel, LoginModel
from src.utilities.parsers import validate_json_body


class UsersController:

    @staticmethod
    def create_user(json_data) -> Users:
        hashed_password = generate_password_hash(json_data["password"]).decode("utf-8")
        subscription_model_id = SubscriptionModelsRepository.get_subscription_model_id(json_data["subscription_model"])

        return Users(user_id=str(ULID()), username=json_data["username"],  # type: ignore
                     name=json_data["name"], email=json_data["email"],
                     password=hashed_password, age=json_data.get("age", None),
                     gender=json_data.get("gender", None),
                     subscription_date=str(datetime.datetime.now()),  # type: ignore
                     subscription_model_id=subscription_model_id,  # type: ignore
                     privacy_policy=json_data["privacy_policy"],
                     terms_and_conditions=json_data["terms_and_conditions"],
                     marketing_consent=json_data["marketing_consent"])

    @classmethod
    def register_user(cls) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        validation_errors = validate_json_body(json_data, RegistrationModel)  # type: ignore
        if validation_errors:
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_user(json_data))

        return {"message": "user added to db"}, 200

    @classmethod
    def login_user(cls):
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

        return {"message": "user logged in"}, 200

    @classmethod
    def check_if_user_exists(cls, json_data) -> Users | None:
        email_or_username = json_data["email_or_username"]

        if user := UsersRepository.get_user_by_username(email_or_username):
            return user

        elif user := UsersRepository.get_user_by_email(email_or_username):
            return user

        return None
