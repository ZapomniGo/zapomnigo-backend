from datetime import datetime
from typing import List

from flask import request
from ulid import ULID

from src.controllers.utility_controller import UtilityController
from src.database.models import Folders, FoldersSets
from src.database.repositories.common_repository import CommonRepository
from src.pydantic_models.folders_model import FoldersModel
from src.utilities.parsers import validate_json_body


class FoldersController:
    @classmethod
    def create_folder(cls, json_data, user_id: str):
        folder_description = json_data.get("folder_description", None)
        category_id = json_data.get("category_id", None)
        organization_id = json_data.get("organization_id", None)

        if folder_description == "":
            folder_description = None
        if category_id == "":
            category_id = None
        if organization_id == "":
            organization_id = None

        return Folders(folder_id=str(ULID()), folder_title=json_data["folder_title"],
                       folder_description=folder_description,
                       folder_modification_date=str(datetime.now()),
                       category_id=category_id,
                       user_id=user_id,
                       organization_id=organization_id)

    @classmethod
    def create_folder_sets(cls, json_data, folder_obj_id: str) -> List[FoldersSets]:
        folder_sets_objects = []
        for set_id in json_data["sets"]:
            folder_sets_objects.append(FoldersSets(folder_set_id=str(ULID()), folder_id=folder_obj_id, set_id=set_id))

        return folder_sets_objects

    @classmethod
    def add_folder(cls):
        json_data = request.json
        user_id = UtilityController.get_session_username_or_user_id(get_username=False)

        if not user_id:
            return {"message": "No token provided"}, 499

        if validation_errors := validate_json_body(json_data, FoldersModel):
            return {"validation errors": validation_errors}, 422

        folder_obj = cls.create_folder(json_data, user_id)
        CommonRepository.add_object_to_db(folder_obj)

        folder_sets = cls.create_folder_sets(json_data, folder_obj.folder_id)
        CommonRepository.add_many_objects_to_db(folder_sets)

        return {"folder_id": folder_obj.folder_id}, 200

    @classmethod
    def get_all_sets_in_folder(cls, folder_id: str):
        pass

    @classmethod
    def get_all_folders_for_user(cls, user_id: str):
        pass

    @classmethod
    def edit_folder(cls, folder_id):
        pass

    @classmethod
    def delete_folder(cls, folder_id):
        pass