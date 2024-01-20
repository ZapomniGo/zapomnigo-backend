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
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.pydantic_models.sets_model import SetsModel, UpdateSetsModel
from src.utilities.parsers import validate_json_body, arg_to_bool


class SetsController:
    @classmethod
    def create_set(cls, json_data: SetsModel, user_id: str) -> Sets:
        return Sets(set_id=str(ULID()), set_name=json_data.set_name,
                    set_description=json_data.set_description,
                    set_modification_date=str(datetime.now()),
                    set_category=json_data.set_category,
                    user_id=user_id,
                    organization_id=json_data.organization_id)

    @classmethod
    def create_flashcards(cls, json_data: SetsModel, set_id: str):
        flashcards_objects = []
        for flashcard in json_data.flashcards:
            flashcards_objects.append(Flashcards(flashcard_id=str(ULID()), term=flashcard.term,
                                                 definition=flashcard.definition,
                                                 notes=flashcard.notes,
                                                 set_id=set_id))
        return flashcards_objects

    @classmethod
    def add_set(cls):
        json_data = request.get_json()
        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        if not user_id:
            return {"message": "No token provided"}, 499

        if validation_errors := validate_json_body(json_data, SetsModel):
            return {"validation errors": validation_errors}, 422

        set_obj = cls.create_set(SetsModel(**json_data), user_id)
        CommonRepository.add_object_to_db(set_obj)

        flashcards = cls.create_flashcards(json_data, set_obj.set_id)
        if len(flashcards) > 2000:
            return {"message": "Cannot create more than 2000 flashcards per set"}, 400

        CommonRepository.add_many_objects_to_db(flashcards)

        return {"set_id": set_obj.set_id}, 200

    @classmethod
    def get_all_sets(cls, user_id: str = "") -> Tuple[Dict[str, Any], int]:
        """If a user_id is passed it gets the sets for a given user"""

        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        sort_by_date = request.args.get('sort_by_date', type=str, default='true')
        ascending = request.args.get('ascending', type=str, default='false')

        sort_by_date = arg_to_bool(sort_by_date)
        ascending = arg_to_bool(ascending)

        result = SetsRepository.get_all_sets(page=page, size=size, user_id=user_id, sort_by_date=sort_by_date,
                                             ascending=ascending)
        sets_list = cls.display_sets_info(result)

        if not sets_list:
            return {"message": "No sets were found"}, 404

        last_page = result.pages if result.pages > 0 else 1

        return {'sets': sets_list, 'total_pages': result.pages, 'current_page': result.page,
                'last_page': last_page}, 200

    @classmethod
    def get_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        if result := SetsRepository.get_set_info(set_id):
            flashcards = FlashcardsRepository.paginate_flashcards_for_set(set_id, page, size)
            last_page = flashcards.pages if flashcards.pages > 0 else 1

            return {"set": cls.display_sets_info(result, flashcards)[0], 'total_pages': flashcards.pages,
                    'current_page': flashcards.page,
                    'last_page': last_page}, 200

        return {"message": "set with such id doesn't exist"}, 404

    @classmethod
    def get_sets_for_user(cls, user_id: str):
        if not UsersRepository.get_user_by_ulid(user_id):
            return {"message": "user doesn't exist"}, 404

        return cls.get_all_sets(user_id)

    @classmethod
    def display_sets_info(cls, result: Pagination | List[Tuple[...]], flashcards=None) -> List[Dict[str, Any]]:
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
            }
            sets_list.append(set_dict)

        if not flashcards:
            return sets_list

        flashcards_list = []
        for flashcard in flashcards:
            flashcard_dict = {
                'flashcard_id': flashcard.flashcard_id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'notes': flashcard.notes
            }
            flashcards_list.append(flashcard_dict)

        sets_list[0]["flashcards"] = flashcards_list

        return sets_list

    @classmethod
    def display_study_info(cls, flashcards: Pagination) -> List[Dict[str, Any]]:
        flashcards_list = []
        for flashcard in flashcards:
            flashcard_dict = {
                'flashcard_id': flashcard.flashcard_id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'confidence': flashcard.confidence
            }
            flashcards_list.append(flashcard_dict)

        return flashcards_list

    @classmethod
    def update_set(cls, set_id: str):
        json_data = request.get_json()
        set_obj, creator_username = SetsRepository.get_set_by_id_with_creator_username(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        if validation_errors := validate_json_body(json_data, UpdateSetsModel):
            return {"validation errors": validation_errors}, 422

        SetsRepository.edit_set(set_obj, json_data)
        FlashcardsRepository.delete_flashcards_by_set_id(set_id)
        flashcards = cls.create_flashcards(json_data, set_id)
        if len(flashcards) > 2000:
            return {"message": "Cannot create more than 2000 flashcards per set"}, 400

        CommonRepository.add_many_objects_to_db(flashcards)

        return {"message": "set successfully updated"}, 200

    @classmethod
    def delete_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj, creator_username = SetsRepository.get_set_by_id_with_creator_username(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        CommonRepository.delete_object_from_db(set_obj)
        return {"message": "Set successfully deleted"}, 200

    @classmethod
    def copy_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj, _ = SetsRepository.get_set_by_id_with_creator_username(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        new_set_obj = Sets(set_id=str(ULID()), set_name=set_obj.set_name,
                           set_description=set_obj.set_description,
                           set_modification_date=str(datetime.now()),
                           set_category=set_obj.set_category,
                           user_id=AuthFunctionality.get_session_username_or_user_id(request, get_username=False),
                           organization_id=None)

        flashcards = FlashcardsRepository.get_flashcards_by_set_id(set_id)
        new_flashcards = []
        for flashcard in flashcards:
            new_flashcards.append(Flashcards(flashcard_id=str(ULID()), term=flashcard.term,
                                             definition=flashcard.definition,
                                             notes=flashcard.notes,
                                             set_id=new_set_obj.set_id))

        CommonRepository.add_object_to_db(new_set_obj)
        CommonRepository.add_many_objects_to_db(new_flashcards)

        return {"set_id": new_set_obj.set_id}, 200

    @classmethod
    def study_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj = SetsRepository.get_set_by_id(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        flashcards = FlashcardsRepository.paginate_flashcards_for_set(set_id, page, size, user_id, is_study=True)

        return {"flashcards": cls.display_study_info(flashcards)}, 200
