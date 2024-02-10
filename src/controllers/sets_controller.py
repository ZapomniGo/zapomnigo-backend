from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict, Any

from flask import request
from ulid import ULID

from src.config import ADMIN_EMAIL
from src.controllers.utility_controller import UtilityController
from src.database.models import Flashcards, ReviewsSets
from src.database.models.sets import Sets
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.flashcards_repository import FlashcardsRepository
from src.database.repositories.sets_repository import SetsRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.common import CommonFunctionality
from src.functionality.mailing_functionality import MailingFunctionality
from src.functionality.sets_functionality import SetsFunctionality
from src.pydantic_models.mail_sender_model import  ReportFolderSetModel
from src.pydantic_models.sets_model import SetsModel, UpdateSetsModel
from src.utilities.parsers import validate_json_body


class SetsController:

    @classmethod
    def add_set(cls):
        json_data = request.get_json()

        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        if not user_id:
            return {"message": "No token provided"}, 499

        if validation_errors := validate_json_body(json_data, SetsModel):
            return {"validation errors": validation_errors}, 422

        set_obj = SetsFunctionality.create_set(SetsModel(**json_data), user_id)
        CommonRepository.add_object_to_db(set_obj)

        flashcards = SetsFunctionality.create_flashcards(SetsModel(**json_data), set_obj.set_id)
        if len(flashcards) > 2000:
            return {"message": "Cannot create more than 2000 flashcards per set"}, 400

        CommonRepository.add_many_objects_to_db(flashcards)

        return {"set_id": set_obj.set_id}, 200

    @classmethod
    def get_all_sets(cls, user_id: str = "") -> Tuple[Dict[str, Any], int]:
        """If a user_id is passed it gets the sets for a given user"""

        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)
        category_id = request.args.get('category_id', type=str)
        subcategory_id = request.args.get('subcategory_id', type=str)

        result = SetsRepository.get_all_sets(page=page, size=size, user_id=user_id, category_id=category_id,
                                             subcategory_id=subcategory_id, sort_by_date=sort_by_date,
                                             ascending=ascending)
        sets_list = SetsFunctionality.display_sets_info(result)

        if not sets_list:
            return {"message": "No sets were found"}, 404

        last_page = result.pages if result.pages > 0 else 1

        return {'sets': sets_list, 'total_pages': result.pages, 'current_page': result.page,
                'last_page': last_page, "total_items": result.total}, 200

    @classmethod
    def get_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)

        if result := SetsRepository.get_set_info(set_id):
            flashcards = FlashcardsRepository.paginate_flashcards_for_set(set_id=set_id, page=page, size=size,
                                                                          sort_by_date=sort_by_date,
                                                                          ascending=ascending)
            last_page = flashcards.pages if flashcards.pages > 0 else 1

            return {"set": SetsFunctionality.display_sets_info(result, flashcards)[0], 'total_pages': flashcards.pages,
                    'current_page': flashcards.page, 'total_items': flashcards.total, 'last_page': last_page}, 200

        return {"message": "set with such id doesn't exist"}, 404

    @classmethod
    def get_sets_for_user(cls, user_id: str):
        if not UsersRepository.get_user_by_ulid(user_id):
            return {"message": "user doesn't exist"}, 404

        return cls.get_all_sets(user_id)

    @classmethod
    def update_set(cls, set_id: str):
        json_data = request.get_json()
        set_obj, creator_username = CommonRepository.get_set_or_folder_by_id_with_creator_username(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        if validation_errors := validate_json_body(json_data, UpdateSetsModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.edit_object(set_obj, UpdateSetsModel(**json_data), field_to_drop="flashcards")
        FlashcardsRepository.delete_flashcards_by_set_id(set_id)

        flashcards = SetsFunctionality.create_flashcards(SetsModel(**json_data), set_id)
        if len(flashcards) > 2000:
            return {"message": "Cannot create more than 2000 flashcards per set"}, 400

        CommonRepository.add_many_objects_to_db(flashcards)

        return {"message": "set successfully updated"}, 200

    @classmethod
    def delete_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj, creator_username = CommonRepository.get_set_or_folder_by_id_with_creator_username(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        FlashcardsRepository.delete_flashcards_by_set_id(set_id)
        CommonRepository.delete_object_from_db(set_obj)
        return {"message": "Set successfully deleted"}, 200

    @classmethod
    def copy_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj = SetsRepository.get_set_by_id(set_id)

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

        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)

        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        flashcards = FlashcardsRepository.paginate_flashcards_for_set(set_id=set_id, page=page, size=size,
                                                                      user_id=user_id, is_study=True,
                                                                      sort_by_date=sort_by_date, ascending=ascending)

        return {"flashcards": SetsFunctionality.display_study_info(flashcards)}, 200

    @classmethod
    def create_studied_set(cls, set_id):
        set_obj = SetsRepository.get_set_by_id(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)

        studied_set = ReviewsSets(review_set_id=str(ULID()), user_id=user_id, set_id=set_id,
                                  review_date=str(datetime.now()))
        CommonRepository.add_object_to_db(studied_set)

        return {"message": "studied set successfully created"}, 200

    @classmethod
    async def report_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, ReportFolderSetModel):
            return {"validation errors": validation_errors}, 422

        username = AuthFunctionality.get_session_username_or_user_id(request)
        if not username:
            return {"message": "No token provided"}, 499

        set_obj = SetsRepository.get_set_by_id(set_id)
        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        report_body = (f"Потребител  {username} докладва тесте {set_obj.set_name} с линк: https://zapomnigo.com/app/set/{set_id} на дата "
                       f"{datetime.now(tz=timezone(timedelta(hours=2))).strftime('%Y-%m-%d %H:%M:%S')} поради следната "
                       f"причина:\n{json_data['reason']}")

        await MailingFunctionality.send_mail_logic(ADMIN_EMAIL, username, is_verification=False, is_report=True,
                                                   report_body=report_body)

        return {"message": "Report sent successfully"}, 200
