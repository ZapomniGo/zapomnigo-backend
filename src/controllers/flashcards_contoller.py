from typing import Tuple, Dict, Any

from flask import request

from src.controllers.utility_controller import UtilityController
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.flashcards_repository import FlashcardsRepository
from src.database.repositories.sets_repository import SetsRepository
from src.pydantic_models.flashcards_model import UpdateFlashcardsModel
from src.utilities.parsers import validate_json_body


class FlashcardsController:
    @classmethod
    def get_all_flashcards(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        if not SetsRepository.get_set_by_id(set_id):
            return {"message": "Set with such id doesn't exist"}, 404

        if result := FlashcardsRepository.get_flashcards_by_set_id(set_id):
            return {"Flashcards": [flashcard.to_json() for flashcard in result]}, 200

        return {"message": "No flashcards were found for this set"}, 404

    @classmethod
    def get_flashcard(cls, flashcard_id: str) -> Tuple[Dict[str, Any], int]:
        if flashcard := FlashcardsRepository.get_flashcard_by_id(flashcard_id):
            return {"flashcard": flashcard.to_json()}, 200

        return {"message": "Flashcard with such id doesn't exist"}, 404

    @classmethod
    def check_if_user_can_delete_flashcard(cls, set_id: str):
        set_obj = SetsRepository.get_set_by_id(set_id)
        if not set_obj:
            return {"message": "Set with such id doesn't exist"}, 404

        username = SetsRepository.get_creator_username(set_obj.get_user_id())
        if result := UtilityController.check_user_access(username):
            return result

    @classmethod
    def update_flashcard(cls, flashcard_id: str):
        json_data = request.get_json()
        flashcard = FlashcardsRepository.get_flashcard_by_id(flashcard_id)

        if not flashcard:
            return {"message": "Flashcard with such id doesn't exist"}, 404

        cls.check_if_user_can_delete_flashcard(flashcard.set_id)

        if validation_errors := validate_json_body(json_data, UpdateFlashcardsModel):  # type: ignore
            return {"validation errors": validation_errors}, 422

        FlashcardsRepository.edit_flashcard(flashcard, json_data)
        return {"message": "Flashcard successfully updated"}, 200

    @classmethod
    def delete_flashcard(cls, flashcard_id: str) -> Tuple[Dict[str, Any], int]:
        flashcard = FlashcardsRepository.get_flashcard_by_id(flashcard_id)

        if not flashcard:
            return {"message": "Flashcard with such id doesn't exist"}, 404

        cls.check_if_user_can_delete_flashcard(flashcard.set_id)

        CommonRepository.delete_object_from_db(flashcard)
        return {"message": "Flashcard successfully deleted"}, 200
