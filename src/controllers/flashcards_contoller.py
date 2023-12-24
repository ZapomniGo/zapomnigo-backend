from flask import request
from ulid import ULID

from src.database.models import Flashcards
from src.database.repositories.common_repository import CommonRepository
from src.pydantic_models.flashcards_model import FlashcardsModel
from src.utilities.parsers import validate_json_body


class FlashcardsController:
    @classmethod
    def create_flashcard(cls, json_data):
        return Flashcards(flashcard_id=str(ULID()), term=json_data["term"],
                          definition=json_data["definition"],
                          notes=json_data.get("notes", None),
                          set_id=json_data["set_id"])

    @classmethod
    def add_flashcard(cls):
        json_data = request.json
        if validation_errors := validate_json_body(json_data, FlashcardsModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        CommonRepository.add_object_to_db(cls.create_flashcard(json_data))

        return {"message": "Flashcard added to db"}, 200

    # @classmethod
    # def get_all_sets(cls) -> Tuple[Dict[str, Any], int]:
    #     if result := CommonRepository.get_all_objects_from_db(Sets):
    #         return {"sets": [sets.to_json(SetsRepository.get_creator_username(sets.get_user_id()))
    #                          for sets in result]}, 200
    #
    #     return {"message": "No sets were found"}, 404
    #
    # @classmethod
    # def get_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
    #     if set_obj := SetsRepository.get_set_by_id(set_id):
    #         username = SetsRepository.get_creator_username(set_obj.get_user_id())
    #         return {"set": set_obj.to_json(username)}, 200
    #
    #     return {"message": "set with such id doesn't exist"}, 404
    #
    # @classmethod
    # def update_set(cls, set_id: str):
    #     json_data = request.get_json()
    #     set_obj = SetsRepository.get_set_by_id(set_id)
    #
    #     if not set_obj:
    #         return {"message": "set with such id doesn't exist"}, 404
    #
    #     username = SetsRepository.get_creator_username(set_obj.get_user_id())
    #     if result := UtilityController.check_user_access(username):
    #         return result
    #
    #     if validation_errors := validate_json_body(json_data, UpdateSetsModel):  # type: ignore
    #         return {"validation errors": validation_errors}, 422
    #
    #     SetsRepository.edit_set(set_obj, json_data)
    #     return {"message": "set successfully updated"}, 200
    #
    # @classmethod
    # def delete_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
    #     set_obj = SetsRepository.get_set_by_id(set_id)
    #
    #     if not set_obj:
    #         return {"message": "set with such id doesn't exist"}, 404
    #
    #     username = SetsRepository.get_creator_username(set_obj.get_user_id())
    #     if result := UtilityController.check_user_access(username):
    #         return result
    #
    #     CommonRepository.delete_object_from_db(set_obj)
    #     return {"message": "Set successfully deleted"}, 200
