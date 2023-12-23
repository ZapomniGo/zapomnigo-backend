from datetime import datetime
from typing import Tuple, Dict, Any

from flask import request
from jwt import decode
from ulid import ULID

from src.config import SECRET_KEY
from src.database.models.sets import Sets
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.users_repository import UsersRepository

from src.pydantic_models.sets_model import SetsModel
from src.utilities.parsers import validate_json_body


class SetsController:
    @classmethod
    def create_set(cls, json_data, user_id: str):
        return Sets(set_id=str(ULID()), set_name=json_data["set_name"],
                    set_description=json_data.get("set_description", None),
                    set_modification_date=str(datetime.now()),
                    set_category=json_data.get("set_category", None),
                    user_id=user_id)

    @classmethod
    def add_set(cls):
        json_data = request.json
        decoded_token = decode(request.cookies.get('refresh_token'), SECRET_KEY, algorithms=["HS256"])
        user_id = UsersRepository.get_user_by_username(decoded_token.get("username")).user_id

        if validation_errors := validate_json_body(json_data, SetsModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_set(json_data, user_id))

        return {"message": "Set added to db"}, 200

    @classmethod
    def get_all_sets(cls) -> Tuple[Dict[str, Any], int]:
        if result := CommonRepository.get_all_objects_from_db(Sets):
            return {"sets": [sets.to_json() for sets in result]}, 200

        return {"message": "No sets were found"}, 404
