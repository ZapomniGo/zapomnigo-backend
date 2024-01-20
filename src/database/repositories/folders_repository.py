from datetime import datetime
from typing import List, Tuple

from sqlalchemy import delete

from src.database.models import Folders, FoldersSets, Users
from src.database.models.base import db
from src.database.repositories.users_repository import UsersRepository
from src.pydantic_models.folders_model import UpdateFoldersModel
from src.utilities.parsers import filter_none_values


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
    def edit_folder(cls, folder_obj: Folders, json_data: UpdateFoldersModel) -> None:
        fields_to_be_updated = filter_none_values(json_data)
        # I drop the sets from the request body as I need only the folders attributes
        fields_to_be_updated.pop("sets")

        for field_name, value in fields_to_be_updated.items():
            setattr(folder_obj, field_name, value)

        folder_obj.folder_modification_date = str(datetime.now())

        db.session.commit()
