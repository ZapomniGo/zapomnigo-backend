from datetime import datetime
from typing import Tuple, Dict, Any

from flask import request
from ulid import ULID

from src.controllers.utility_controller import UtilityController
from src.database.models import Flashcards
from src.database.models.sets import Sets
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.flashcards_repository import FlashcardsRepository
from src.database.repositories.sets_repository import SetsRepository
from src.database.repositories.users_repository import UsersRepository
from src.pydantic_models.sets_model import SetsModel, UpdateSetsModel
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
    def create_flashcards(cls, json_data, set_id: str):
        flashcards_objects = []
        for flashcard in json_data.get("flashcards", []):
            flashcards_objects.append(Flashcards(flashcard_id=str(ULID()), term=flashcard["term"],
                                                 definition=flashcard["definition"],
                                                 notes=flashcard.get("notes", None),
                                                 set_id=set_id))
        return flashcards_objects

    @classmethod
    def add_set(cls):
        json_data = request.json
        user_id = UsersRepository.get_user_by_username(UtilityController.get_session_username()).user_id
        if validation_errors := validate_json_body(json_data, SetsModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        set_obj = cls.create_set(json_data, user_id)
        CommonRepository.add_object_to_db(set_obj)

        flashcards = cls.create_flashcards(json_data, set_obj.set_id)
        if len(flashcards) > 2000:
            return {"message": "Cannot create more than 2000 flashcards per set"}, 400

        CommonRepository.add_many_objects_to_db(flashcards)

        return {"message": "Set added to db"}, 200

    @classmethod
    def get_all_sets(cls) -> Tuple[Dict[str, Any], int]:
        if result := CommonRepository.get_all_objects_from_db(Sets):
            return {"sets": [sets.to_json(SetsRepository.get_creator_username(sets.get_user_id()))
                             for sets in result]}, 200

        return {"message": "No sets were found"}, 404

    @classmethod
    def get_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        if set_obj := SetsRepository.get_set_by_id(set_id):
            username = SetsRepository.get_creator_username(set_obj.get_user_id())
            return {"set": set_obj.to_json(username)}, 200

        return {"message": "set with such id doesn't exist"}, 404

    @classmethod
    def update_set(cls, set_id: str):
        json_data = request.get_json()
        set_obj = SetsRepository.get_set_by_id(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        username = SetsRepository.get_creator_username(set_obj.get_user_id())
        if result := UtilityController.check_user_access(username):
            return result

        if validation_errors := validate_json_body(json_data, UpdateSetsModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        SetsRepository.edit_set(set_obj, json_data)

        if flashcards := cls.create_flashcards(json_data, set_obj.set_id):
            if len(FlashcardsRepository.get_flashcards_by_set_id(set_obj.set_id)) + len(flashcards) > 2000:
                return {"message": "Cannot create more than 2000 flashcards per set"}, 400
            else:
                CommonRepository.add_many_objects_to_db(flashcards)

        return {"message": "set successfully updated"}, 200

    @classmethod
    def delete_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj = SetsRepository.get_set_by_id(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        username = SetsRepository.get_creator_username(set_obj.get_user_id())
        if result := UtilityController.check_user_access(username):
            return result

        CommonRepository.delete_object_from_db(set_obj)
        return {"message": "Set successfully deleted"}, 200
