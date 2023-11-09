import datetime

from flask import request
from flask_bcrypt import generate_password_hash
from jsonschema.validators import Draft7Validator
from ulid import ULID

from src.database.models import Users
from src.utilities.json_schemas import register_schema


class UsersControllers:

    @staticmethod
    def create_user(json_data):
        hashed_password = generate_password_hash(json_data["password"]).decode("utf-8")

        return Users(user_id=str(ULID), username=json_data["username"],  # type: ignore
                     name=json_data["name"], email=json_data["email"],
                     password=hashed_password, age=json_data.get("age", None),
                     gender=json_data.get("gender", None),
                     subscription_date=str(datetime.datetime.now()),  # type: ignore
                     privacy_policy=json_data["privacy_policy"],
                     terms_and_conditions=json_data["terms_and_conditions"],
                     marketing_consent=json_data["marketing_consent"])

    @classmethod
    def register_user(cls):
        json_data = request.get_json()
        user = cls.create_user(json_data)
        errors = cls.format_validation_errors(json_data)
        return {"validation errors": errors}, 400

    @classmethod
    def format_validation_errors(cls, data):
        validator = Draft7Validator(register_schema)
        errors = []
        for error in validator.iter_errors(data):
            errors.append(error.message.replace("'", "").replace("is a", "").replace("is", "").replace("  ", " "))
        return errors
