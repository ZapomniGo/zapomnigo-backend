from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict, Any

from flask import request

from src.config import ADMIN_EMAIL
from src.controllers.utility_controller import UtilityController
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.folders_repository import FoldersRepository
from src.database.repositories.sets_repository import SetsRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.common import CommonFunctionality
from src.functionality.folders_functionallity import FoldersFunctionality
from src.functionality.mailing_functionality import MailingFunctionality
from src.functionality.sets_functionality import SetsFunctionality
from src.pydantic_models.common import VerifySetFolderModel
from src.pydantic_models.folders_model import FoldersModel, UpdateFoldersModel
from src.pydantic_models.mail_sender_model import ReportFolderSetModel
from src.utilities.parsers import validate_json_body


class FoldersController:

    @classmethod
    def add_folder(cls):
        json_data = request.get_json()

        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        if not user_id:
            return {"message": "No token provided"}, 499

        if validation_errors := validate_json_body(json_data, FoldersModel):
            return {"validation errors": validation_errors}, 422

        folder_obj = FoldersFunctionality.create_folder(FoldersModel(**json_data), user_id)
        CommonRepository.add_object_to_db(folder_obj)

        folder_sets = FoldersFunctionality.create_folder_sets(json_data["sets"], folder_obj.folder_id)
        CommonRepository.add_many_objects_to_db(folder_sets)

        return {"folder_id": folder_obj.folder_id}, 200

    @classmethod
    def get_all_folders(cls, user_id: str = "") -> Tuple[Dict[str, Any], int]:
        """If a user_id is passed it gets the folders for a given user"""

        if user_id:
            if not UsersRepository.get_user_by_ulid(user_id):
                return {"message": "user doesn't exist"}, 404

        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)
        category_id = request.args.get('category_id', type=str)
        subcategory_id = request.args.get('subcategory_id', type=str)
        search_terms = request.args.get("search", type=str)

        result = FoldersRepository.get_all_folders(page=page, size=size, user_id=user_id, category_id=category_id,
                                                   subcategory_id=subcategory_id,
                                                   sort_by_date=sort_by_date,
                                                   ascending=ascending, search_terms=search_terms)
        if search_terms:
            return CommonFunctionality.search_format_results(result, []), 200

        folders_list = FoldersFunctionality.display_folders_info(result)

        if not folders_list:
            return {"message": "No Folders were found"}, 404

        return {'folders': folders_list, 'total_pages': result.pages, 'current_page': result.page,
                'total_items': result.total}, 200

    @classmethod
    def get_sets_in_folder(cls, folder_id: str) -> Tuple[Dict[str, Any], int]:
        page, size, sort_by_date, ascending = CommonFunctionality.get_pagination_params(request)

        folder = FoldersRepository.get_folder_info(folder_id)
        if not folder:
            return {"message": "Folder with such id doesn't exist"}, 404
        folder_info = FoldersFunctionality.display_folders_info(folder)[0]

        sets = SetsRepository.get_all_sets(page=page, size=size, folder_id=folder_id, sort_by_date=sort_by_date)
        sets_list = SetsFunctionality.display_sets_info(sets)

        if not sets_list:
            return {"message": "No sets were found"}, 404

        return {"folder": folder_info, 'sets': sets_list, 'total_pages': sets.pages, 'current_page': sets.page}, 200

    @classmethod
    def edit_folder(cls, folder_id: str):
        json_data = request.get_json()

        folder_obj, creator_username = CommonRepository.get_set_or_folder_by_id_with_creator_username(folder_id,
                                                                                                      get_set=False)

        if not folder_obj:
            return {"message": "Folder with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        if validation_errors := validate_json_body(json_data, UpdateFoldersModel):
            return {"validation errors": validation_errors}, 422

        CommonRepository.edit_object(folder_obj, UpdateFoldersModel(**json_data), field_to_drop="sets")
        FoldersRepository.delete_folders_sets_by_folder_id(folder_id)

        folder_sets = FoldersFunctionality.create_folder_sets(json_data["sets"], folder_obj.folder_id)
        CommonRepository.add_many_objects_to_db(folder_sets)

        return {"message": "Folder successfully updated"}, 200

    @classmethod
    def delete_folder(cls, folder_id: str):
        folder_obj, creator_username = CommonRepository.get_set_or_folder_by_id_with_creator_username(folder_id,
                                                                                                      get_set=False)

        if not folder_obj:
            return {"message": "Folder with such id doesn't exist"}, 404

        if result := UtilityController.check_user_access(creator_username):
            return result

        CommonRepository.delete_object_from_db(folder_obj)
        return {"message": "Folder successfully deleted"}, 200

    @classmethod
    async def report_folder(cls, folder_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        if validation_errors := validate_json_body(json_data, ReportFolderSetModel):
            return {"validation errors": validation_errors}, 422

        username = AuthFunctionality.get_session_username_or_user_id(request)
        if not username:
            return {"message": "No token provided"}, 499

        folder_obj = FoldersRepository.get_folder_by_id(folder_id)
        if not folder_obj:
            return {"message": "Folder with such id doesn't exist"}, 404

        report_body = (
            f"Потребител  {username} докладва папка {folder_obj.folder_title} с линк: https://zapomnigo.com/app/folder/{folder_id} на дата "
            f"{datetime.now(tz=timezone(timedelta(hours=2))).strftime('%Y-%m-%d %H:%M:%S')} поради следната "
            f"причина:\n{json_data['reason']}")

        await MailingFunctionality.send_mail_logic(ADMIN_EMAIL, username, is_verification=False, is_report=True,
                                                   report_body=report_body)
        return {"message": "Folder successfully reported"}, 200

    @classmethod
    def change_verified_status_folder(cls, folder_id: str) -> Tuple[Dict[str, Any], int]:
        json_data = request.get_json()

        folder = FoldersRepository.get_folder_by_id(folder_id)
        if not folder:
            return {"message": "Folder with such id doesn't exist"}, 404

        if validation_errors := validate_json_body(json_data, VerifySetFolderModel):
            return {"validation errors": validation_errors}, 422

        FoldersRepository.change_verified_status_folder(folder, json_data["verified"])

        return {"message": "folder verified status changed successfully"}, 200
