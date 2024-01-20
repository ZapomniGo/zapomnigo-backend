from datetime import datetime
from typing import List

from flask import request
from ulid import ULID

from src.controllers.sets_controller import SetsController
from src.controllers.utility_controller import UtilityController
from src.database.models import Folders, FoldersSets
from src.database.repositories.categories_repository import CategoriesRepository
from src.database.repositories.common_repository import CommonRepository
from src.database.repositories.folders_repository import FoldersRepository
from src.database.repositories.organizations_repository import OrganizationsRepository
from src.database.repositories.sets_repository import SetsRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.pydantic_models.folders_model import FoldersModel, UpdateFoldersModel
from src.pydantic_models.sets_model import UpdateSetsModel
from src.utilities.parsers import validate_json_body, arg_to_bool


class FoldersController:
    @classmethod
    def create_folder(cls, json_data: FoldersModel, user_id: str) -> Folders:
        return Folders(folder_id=str(ULID()), folder_title=json_data.folder_title,
                       folder_description=json_data.folder_description,
                       folder_modification_date=str(datetime.now()),
                       category_id=json_data.category_id,
                       user_id=user_id,
                       organization_id=json_data.organization_id)

    @classmethod
    def create_folder_sets(cls, set_ids: List[str], folder_obj_id: str) -> List[FoldersSets]:
        folder_sets_objects = []
        for set_id in set_ids:
            folder_sets_objects.append(FoldersSets(folder_set_id=str(ULID()), folder_id=folder_obj_id, set_id=set_id))

        return folder_sets_objects

    @classmethod
    def add_folder(cls):
        json_data = request.get_json()

        user_id = AuthFunctionality.get_session_username_or_user_id(request, get_username=False)
        if not user_id:
            return {"message": "No token provided"}, 499

        if validation_errors := validate_json_body(json_data, FoldersModel):
            return {"validation errors": validation_errors}, 422

        folder_obj = cls.create_folder(FoldersModel(**json_data), user_id)
        CommonRepository.add_object_to_db(folder_obj)

        folder_sets = cls.create_folder_sets(json_data["sets"], folder_obj.folder_id)
        CommonRepository.add_many_objects_to_db(folder_sets)

        return {"folder_id": folder_obj.folder_id}, 200

    @classmethod
    def get_all_sets_in_folder(cls, folder_id: str):
        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        sort_by_date = request.args.get('sort_by_date', type=str, default='true')
        ascending = request.args.get('ascending', type=str, default='false')

        sort_by_date = arg_to_bool(sort_by_date)
        ascending = arg_to_bool(ascending)

        folder = FoldersRepository.get_folder_by_id(folder_id)
        if not folder:
            return {"message": "Folder with such id doesn't exist"}, 404

        result = SetsRepository.get_all_sets(page=page, size=size, folder_id=folder_id, sort_by_date=sort_by_date,
                                             ascending=ascending)
        sets_list = SetsController.display_sets_info(result)
        last_page = result.pages if result.pages > 0 else 1

        return {'folder_title': folder.folder_title, 'folder_description': folder.folder_description,
                'folder_creator': FoldersRepository.get_creator_username(folder.user_id),
                'category_name': CategoriesRepository.get_category_name_by_id(folder.category_id),
                "organization_name": OrganizationsRepository.get_organization_name_by_id(folder.organization_id),
                'sets': sets_list, 'pagination_of_sets': {'total_pages': result.pages, 'current_page': result.page,
                                                          'last_page': last_page}}, 200

    @classmethod
    def get_all_folders_for_user(cls, user_id: str):
        if not UsersRepository.get_user_by_ulid(user_id):
            return {"message": "user doesn't exist"}, 404

        if result := FoldersRepository.get_folders_by_user_id(user_id):
            return {"folders": [folders.to_json(FoldersRepository.get_creator_username(folders.user_id))
                                for folders in result]}, 200

        return {"message": "No folders were found for the given user"}, 404

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

        FoldersRepository.edit_folder(folder_obj, UpdateFoldersModel(**json_data))
        FoldersRepository.delete_folders_sets_by_folder_id(folder_id)

        folder_sets = cls.create_folder_sets(json_data["sets"], folder_obj.folder_id)
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
