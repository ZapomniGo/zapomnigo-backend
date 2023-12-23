from datetime import datetime
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
    def edit_set(cls, set_obj: Sets, json_data: Dict[str, Any]) -> None:
        set_obj.set_name = json_data.get("set_name", set_obj.set_name)
        set_obj.set_description = json_data.get("set_description", set_obj.set_description)
        set_obj.set_modification_date = str(datetime.now())

        try:
            # Checks for falsify values like "" and None
            if not json_data["set_category"]:
                set_obj.set_category = None
            else:
                set_obj.set_category = json_data["set_category"]
        except KeyError:
            set_obj.set_category = set_obj.set_category

        db.session.commit()
