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
from src.database.repositories.folders_repository import FoldersRepository
from src.database.repositories.sets_repository import SetsRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.common import CommonFunctionality
from src.functionality.folders_functionallity import FoldersFunctionality
from src.functionality.mailing_functionality import MailingFunctionality
from src.functionality.sets_functionality import SetsFunctionality
from src.pydantic_models.common import VerifySetFolderModel
from src.pydantic_models.mail_sender_model import ReportFolderSetModel
from src.pydantic_models.sets_model import SetsModel, UpdateSetsModel
from src.utilities.parsers import validate_json_body


class SetsController:

    @classmethod
    def add_set(cls) -> Tuple[Dict[str, Any], int]:
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

        folder_id = request.args.get('folder_id', type=str)
        if folder_id:
            _, username = CommonRepository.get_set_or_folder_by_id_with_creator_username(folder_id, get_set=False)

            if result := UtilityController.check_user_access(username):
                return result

            folder_set = FoldersFunctionality.create_folder_sets([set_obj.set_id], folder_id)
            CommonRepository.add_many_objects_to_db(folder_set)

        return {"set_id": set_obj.set_id}, 200

    @classmethod
    def get_all_sets(cls, user_id: str = "") -> Tuple[Dict[str, Any], int]:
        """If a user_id is passed it gets the sets for a given user"""

        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)
        category_id = request.args.get('category_id', type=str)
        subcategory_id = request.args.get('subcategory_id', type=str)
        search_terms = request.args.get("search", type=str)

        result = SetsRepository.get_all_sets(page=page, size=size, user_id=user_id, category_id=category_id,
                                             subcategory_id=subcategory_id, sort_by_date=sort_by_date,
                                             ascending=ascending, search_terms=search_terms)
        if search_terms:
            return CommonFunctionality.search_format_results([], result), 200

        sets_list = SetsFunctionality.display_sets_info(result)

        if not sets_list:
            return {"message": "No sets were found"}, 404

        return {'sets': sets_list, 'total_pages': result.pages, 'current_page': result.page,
                "total_items": result.total}, 200

    @classmethod
    def get_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)

        if result := SetsRepository.get_set_info(set_id):
            flashcards = FlashcardsRepository.paginate_flashcards_for_set(set_id=set_id, page=page, size=size,
                                                                          sort_by_date=sort_by_date,
                                                                          ascending=ascending)

            return {"set": SetsFunctionality.display_sets_info(result, flashcards)[0], 'total_pages': flashcards.pages,
                    'current_page': flashcards.page, 'total_items': flashcards.total}, 200

        return {"message": "set with such id doesn't exist"}, 404

    @classmethod
    def get_sets_for_user(cls, user_id: str):
        if not UsersRepository.get_user_by_ulid(user_id):
            return {"message": "user doesn't exist"}, 404

        return cls.get_all_sets(user_id)

    @classmethod
    def update_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()
        set_obj, creator_username = CommonRepository.get_set_or_folder_by_id_with_creator_username(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        if validation_errors := validate_json_body(json_data, UpdateSetsModel):
            return {"validation errors": validation_errors}, 422

        # As we are passing the flashcards in the update body, we have to drop the field because it is not part of
        # the original Sets SQLAlchemy object
        CommonRepository.edit_object(set_obj, UpdateSetsModel(**json_data), fields_to_drop=["flashcards"])
        FlashcardsRepository.delete_flashcards_by_set_id(set_id)

        flashcards = SetsFunctionality.create_flashcards(SetsModel(**json_data), set_id)
        if len(flashcards) > 2000:
            return {"message": "Cannot create more than 2000 flashcards per set"}, 400

        CommonRepository.add_many_objects_to_db(flashcards)

        folder_id = request.args.get('folder_id', type=str)
        if folder_id:
            _, username = CommonRepository.get_set_or_folder_by_id_with_creator_username(folder_id, get_set=False)

            if result := UtilityController.check_user_access(username):
                return result

            folder_set = FoldersFunctionality.create_folder_sets([set_obj.set_id], folder_id)
            CommonRepository.add_many_objects_to_db(folder_set)

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

        report_body = (
            f"Потребител  {username} докладва тесте {set_obj.set_name} с линк: https://zapomnigo.com/app/set/{set_id} на дата "
            f"{datetime.now(tz=timezone(timedelta(hours=2))).strftime('%Y-%m-%d %H:%M:%S')} поради следната "
            f"причина:\n{json_data['reason']}")

        await MailingFunctionality.send_report_email(ADMIN_EMAIL, report_body)

        return {"message": "Report sent successfully"}, 200

    @classmethod
    def change_verified_status_set(cls, set_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        set_obj = SetsRepository.get_set_by_id(set_id)

        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        if validation_errors := validate_json_body(json_data, VerifySetFolderModel):
            return {"validation errors": validation_errors}, 422

        SetsRepository.change_verified_status_set(set_obj, json_data["verified"])

        return {"message": "set verified status changed successfully"}, 200

    @classmethod
    def add_set_to_folder(cls, set_id: str, folder_id: str) -> Tuple[Dict[str, Any], int]:
        set_obj = SetsRepository.get_set_by_id(set_id)
        if not set_obj:
            return {"message": "set with such id doesn't exist"}, 404

        folder_obj = FoldersRepository.get_folder_by_id(folder_id)
        if not folder_obj:
            return {"message": "folder with such id doesn't exist"}, 404

        _, username = CommonRepository.get_set_or_folder_by_id_with_creator_username(folder_id, get_set=False)

        if result := UtilityController.check_user_access(username):
            return result

        folder_set = FoldersFunctionality.create_folder_sets([set_id], folder_id)
        CommonRepository.add_many_objects_to_db(folder_set)

        return {"message": "set successfully added to folder"}, 200
