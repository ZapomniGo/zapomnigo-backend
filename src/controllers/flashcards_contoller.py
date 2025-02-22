from typing import Tuple, Dict, Any

from flask import request
from ulid import ULID

from src.controllers.utility_controller import UtilityController
from src.database.database_transaction_handlers import handle_database_session_transaction
from src.database.models import ReviewsFlashcards
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.flashcards_repository import FlashcardsRepository
from src.database.repositories.reviews_flashcards_repository import ReviewsFlashcardsRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.pydantic_models.flashcards_model import UpdateFlashcardsModel, StudyFlashcardsModel
from src.utilities.parsers import validate_json_body


class FlashcardsController:

    @classmethod
    def get_flashcard(cls, flashcard_id: str) -> Tuple[Dict[str, Any], int]:
        if flashcard := FlashcardsRepository.get_flashcard_by_id(flashcard_id):
            return {"flashcard": flashcard.single_to_json()}, 200

        return {"message": "Flashcard with such id doesn't exist"}, 404

    @classmethod
    def check_if_user_can_edit_or_delete_flashcard(cls, set_id: str):
        set_obj, creator_username = CommonRepository.get_set_or_folder_by_id_with_creator_username(set_id)
        if not set_obj:
            return {"message": "Set with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

    @classmethod
    @handle_database_session_transaction
    def update_flashcard(cls, flashcard_id: str):
        json_data = request.get_json()
        flashcard = FlashcardsRepository.get_flashcard_by_id(flashcard_id)

        if not flashcard:
            return {"message": "Flashcard with such id doesn't exist"}, 404

        if result := cls.check_if_user_can_edit_or_delete_flashcard(flashcard.set_id):
            return result

        if validation_errors := validate_json_body(json_data, UpdateFlashcardsModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.edit_object(flashcard, UpdateFlashcardsModel(**json_data))
        return {"message": "Flashcard successfully updated"}, 200

    @classmethod
    @handle_database_session_transaction
    def delete_flashcard(cls, flashcard_id: str) -> Tuple[Dict[str, Any], int]:
        flashcard = FlashcardsRepository.get_flashcard_by_id(flashcard_id)

        if not flashcard:
            return {"message": "Flashcard with such id doesn't exist"}, 404

        if result := cls.check_if_user_can_edit_or_delete_flashcard(flashcard.set_id):
            return result

        CommonRepository.delete_object_from_db(flashcard)
        return {"message": "Flashcard successfully deleted"}, 200

    @classmethod
    @handle_database_session_transaction
    def study_flashcard(cls, flashcard_id):
        json_data = request.get_json()
        flashcard = FlashcardsRepository.get_flashcard_by_id(flashcard_id)

        if not flashcard:
            return {"message": "Flashcard with such id doesn't exist"}, 404

        if validation_errors := validate_json_body(json_data, StudyFlashcardsModel):
            return {"validation errors": validation_errors}, 422

        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        if not user_id:
            return {"message": "user_id is not provided in the auth token"}, 499

        # Here it's just faster to get the user_id from the raw json instead through the pydantic model
        if result := ReviewsFlashcardsRepository.get_review_by_flashcard_id(flashcard_id, user_id):
            ReviewsFlashcardsRepository.edit_review_flashcard(result, StudyFlashcardsModel(**json_data))

        else:
            study_flashcard_obj = ReviewsFlashcards(reviews_flashcards_id=str(ULID()), user_id=user_id,
                                                    flashcard_id=flashcard_id, confidence=0)
            CommonRepository.add_object_to_db(study_flashcard_obj)

        return {"message": "Confidence level of flashcard updated!"}, 200
