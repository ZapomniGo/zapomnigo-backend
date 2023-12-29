from datetime import datetime
from typing import Tuple, Dict, Any, List

from flask import request
from flask_sqlalchemy.pagination import Pagination
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
        set_description = json_data.get("set_description", None)
        set_category = json_data.get("set_category", None)
        organization_id = json_data.get("organization_id", None)

        if set_description == "":
            set_description = None
        if set_category == "":
            set_category = None
        if organization_id == "":
            organization_id = None

        return Sets(set_id=str(ULID()), set_name=json_data["set_name"],
                    set_description=set_description,
                    set_modification_date=str(datetime.now()),
                    set_category=set_category,
                    user_id=user_id,
                    organization_id=organization_id)

    @classmethod
    def create_flashcards(cls, json_data, set_id: str):
        flashcards_objects = []
        for flashcard in json_data.get("flashcards", []):
            notes = flashcard.get("notes", None)
            if notes == "":
                notes = None

            flashcards_objects.append(Flashcards(flashcard_id=str(ULID()), term=flashcard["term"],
                                                 definition=flashcard["definition"],
                                                 notes=notes,
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

        return {"set_id": set_obj.set_id}, 200

    @classmethod
    def get_all_flashcards_for_set(cls, set_id: str) -> List[Dict[str, Any]]:
        return [flashcard.to_json() for flashcard in FlashcardsRepository.get_flashcards_by_set_id(set_id)]

    @classmethod
    def get_all_sets(cls, user_id: str = "") -> Tuple[Dict[str, Any], int]:
        page = request.args.get('page', type=int)
        per_page = request.args.get('size', type=int)
        result = SetsRepository.get_all_sets(page, per_page, user_id)
        if not result:
            return {"message": "No sets were found"}, 404

        sets_list = cls.display_sets_info(result)
        last_page = result.pages if result.pages > 0 else 1

        return {'sets': sets_list, 'total_pages': result.pages, 'current_page': result.page,
                'last_page': last_page}, 200

    @classmethod
    def get_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        if result := SetsRepository.get_set_info(set_id):
            return {"set": cls.display_sets_info(result)}, 200

        return {"message": "set with such id doesn't exist"}, 404

    @classmethod
    def get_sets_for_user(cls, user_id: str):
        if not UsersRepository.get_user_by_ulid(user_id):
            return {"message": "user doesn't exist"}, 404

        return cls.get_all_sets(user_id)

    @classmethod
    def display_sets_info(cls, result: Pagination | List[Tuple[...]]) -> List[Dict[str, Any]]:
        sets_list = []
        for row in result:
            set_dict = {
                'set_id': row.set_id,
                'set_name': row.set_name,
                'set_description': row.set_description,
                'set_modification_date': row.set_modification_date,
                'category_name': row.category_name,
                'organization_name': row.organization_name,
                'username': row.username,
                'flashcards': []
            }

            flashcard_dict = {
                'flashcard_id': row.flashcard_id,
                'term': row.term,
                'definition': row.definition,
                'notes': row.notes
            }

            set_dict['flashcards'].append(flashcard_dict)
            sets_list.append(set_dict)

        return sets_list

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
