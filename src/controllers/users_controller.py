from flask import request
from jsonschema.validators import Draft7Validator

from src.utilities.json_schemas import register_schema


class UsersControllers:

    @staticmethod
    def create_user(json_data):
        pass

    @classmethod
    def register_user(cls):
        data = request.get_json()

        errors = cls.format_validation_errors(data)
        return {"validation errors": errors}, 400

    @classmethod
    def format_validation_errors(cls, data):
        validator = Draft7Validator(register_schema)
        errors = []
        for error in validator.iter_errors(data):
            errors.append(error.message.replace("'", "").replace("is a", "").replace("is", "").replace("  ", " "))
        return errors
