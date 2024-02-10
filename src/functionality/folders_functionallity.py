from datetime import datetime
from typing import List, Tuple, Dict, Any

from flask_sqlalchemy.pagination import Pagination
from ulid import ULID

from src.database.models import Folders, FoldersSets
from src.pydantic_models.folders_model import FoldersModel


class FoldersFunctionality:

    @classmethod
    def create_folder(cls, json_data: FoldersModel, user_id: str) -> Folders:
        return Folders(folder_id=str(ULID()), folder_title=json_data.folder_title,
                       folder_description=json_data.folder_description,
                       folder_modification_date=str(datetime.now()),
                       category_id=json_data.category_id,
                       subcategory_id=json_data.subcategory_id,
                       user_id=user_id,
                       organization_id=json_data.organization_id)

    @classmethod
    def create_folder_sets(cls, set_ids: List[str], folder_obj_id: str) -> List[FoldersSets]:
        folder_sets_objects = []
        for set_id in set_ids:
            folder_sets_objects.append(FoldersSets(folder_set_id=str(ULID()), folder_id=folder_obj_id, set_id=set_id))

        return folder_sets_objects

    @classmethod
    def display_folders_info(cls, result: Pagination | List[Tuple[...]]) -> List[Dict[str, Any]]:
        folders_list = []
        for row in result:
            folder_dict = {
                'folder_id': row.folder_id,
                'folder_title': row.folder_title,
                'folder_description': row.folder_description,
                'folder_modification_date': row.folder_modification_date,
                'category_name': row.category_name,
                "subcategory_name": row.subcategory_name,
                'username': row.username,
                'verified': row.verified
            }
            folders_list.append(folder_dict)

        return folders_list
