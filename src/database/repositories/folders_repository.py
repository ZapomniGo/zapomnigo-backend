from src.database.models import Folders
from src.database.models.base import db
from src.database.repositories.users_repository import UsersRepository


class FoldersRepository:
    @classmethod
    def get_creator_username(cls, user_id: str) -> str:
        return str(UsersRepository.get_user_by_ulid(user_id).username)

    @classmethod
    def get_folder_by_id(cls, folder_id: str) -> Folders | None:
        return db.session.query(Folders).filter_by(folder_id=folder_id).first()