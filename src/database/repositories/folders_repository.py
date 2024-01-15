from datetime import datetime
from typing import Dict, Any, List

from sqlalchemy import delete

from src.database.models import Folders, FoldersSets
from src.database.models.base import db
from src.database.repositories.users_repository import UsersRepository


class FoldersRepository:
    @classmethod
    def get_creator_username(cls, user_id: str) -> str:
        return str(UsersRepository.get_user_by_ulid(user_id).username)

    @classmethod
    def get_folder_by_id(cls, folder_id: str) -> Folders | None:
        return db.session.query(Folders).filter_by(folder_id=folder_id).first()

    @classmethod
    def get_folders_by_user_id(cls, user_id: str) -> List[Folders] | None:
        return db.session.query(Folders).filter_by(user_id=user_id).all()

    @classmethod
    def delete_folders_sets_by_folder_id(cls, folder_id: str) -> None:
        db.session.execute(delete(FoldersSets).where(FoldersSets.folder_id == folder_id))
        db.session.commit()

    @classmethod
    def edit_folder(cls, folder: Folders, json_data: Dict[str, Any]) -> None:
        folder.folder_title = json_data.get("folder_title", folder.folder_title)
        folder.folder_description = json_data.get("folder_description", folder.folder_description)
        folder.folder_title = json_data.get("folder_title", folder.folder_title)
        folder.folder_modification_date = str(datetime.now())

        try:
            # Checks for falsify values like "" and None
            if not json_data["category_id"]:
                folder.category_id = None
            else:
                folder.category_id = json_data["category_id"]
        except KeyError:
            folder.category_id = folder.category_id

        db.session.commit()
