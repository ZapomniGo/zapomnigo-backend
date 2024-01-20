from typing import List

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
