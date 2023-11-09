import datetime
from typing import Tuple, Dict

from flask import request
from flask_bcrypt import generate_password_hash
from ulid import ULID

from src.database.models import Users
from src.pydantic_models.registration_model import RegistrationModel
from src.utilities.parsers import validate_json_body


class UsersControllers:

    @staticmethod
    def create_user(json_data) -> Users:
        hashed_password = generate_password_hash(json_data["password"]).decode("utf-8")

        return Users(user_id=str(ULID()), username=json_data["username"],  # type: ignore
                     name=json_data["name"], email=json_data["email"],
                     password=hashed_password, age=json_data.get("age", None),
                     gender=json_data.get("gender", None),
                     subscription_date=str(datetime.datetime.now()),  # type: ignore
                     privacy_policy=json_data["privacy_policy"],
                     terms_and_conditions=json_data["terms_and_conditions"],
                     marketing_consent=json_data["marketing_consent"])

    @classmethod
    def register_user(cls) -> Tuple[Dict[str, str], int]:
        json_data = request.get_json()
        errors = validate_json_body(json_data, RegistrationModel)  # type: ignore
        if errors:
            return {"validation errors": errors}, 422
        return {"users": cls.create_user(json_data)}, 200
