from typing import Dict, Any

from src.database.models.base import db
from src.database.models.sets import Sets
from src.database.repositories.users_repository import UsersRepository


class SetsRepository:

    @classmethod
    def get_creator_username(cls, user_id: str) -> str:
        return str(UsersRepository.get_user_by_ulid(user_id).username)

    @classmethod
    def get_set_by_id(cls, set_id: str) -> Sets | None:
        return db.session.query(Sets).filter_by(set_id=set_id).first()

    @classmethod
    def edit_set(cls, set: Sets, json_data: Dict[str, Any]) -> None:
        set.set_name = json_data.get("set_name", set.set_name).lower()
        db.session.commit()
