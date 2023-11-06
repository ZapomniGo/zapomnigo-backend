import json

from flask import request, jsonify
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

from src.utilities.json_schemas import register_schema


class UsersControllers:

    @staticmethod
    def create_user(json_data):
        pass

    @classmethod
    def register_user(cls):
        data = request.get_json()

        try:
            validate(data, register_schema)
        except ValidationError as e:
            error_message = "Input data does not conform to the schema: " + str(e)
            return {"error": error_message}, 400
