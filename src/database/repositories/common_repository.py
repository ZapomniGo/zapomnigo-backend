from typing import List, Any, Tuple

from pydantic import BaseModel

from src.database.models import Sets, Folders, Users
from src.database.models.base import db


class CommonRepository:

    @classmethod
    def add_many_objects_to_db(cls, objects: List[Any]) -> None:
        db.session.add_all(objects)

    @classmethod
    def add_object_to_db(cls, obj) -> None:
        db.session.add(obj)

    @classmethod
    def get_all_objects_from_db(cls, obj):
        return db.session.query(obj).all()

    @classmethod
    def delete_object_from_db(cls, obj) -> None:
        db.session.delete(obj)

    @classmethod
    def edit_object(cls, obj, json_data: BaseModel, fields_to_drop: List[str] | None = None) -> None:

        fields_to_be_updated = json_data.model_dump()
        print(fields_to_be_updated)
        if fields_to_drop is None:
            fields_to_drop = []

        # As the fields which are not passed in the body are None,
        # we should drop them from the update
        # for key, value in fields_to_be_updated.items():
        #     if value is None:
        #         fields_to_drop.append(key)

        # This filed is dropped from the req body as it is not part of the original SQLAlchemy obj
        for field in fields_to_drop:
            fields_to_be_updated.pop(field, None)

        for field_name, value in fields_to_be_updated.items():
            setattr(obj, field_name, value)

    @classmethod
    def get_set_or_folder_by_id_with_creator_username(cls, set_or_folder_id: str, get_set=True) -> Tuple[
        (Sets | Folders) | None, str | None]:

        entity_class = Sets if get_set else Folders
        entity_key = "set_id" if get_set else "folder_id"

        entity_info = db.session.query(entity_class, Users.username) \
            .join(Users, entity_class.user_id == Users.user_id) \
            .filter(getattr(entity_class, entity_key) == set_or_folder_id) \
            .first()

        if entity_info:
            entity_obj, creator_username = entity_info
            return entity_obj, creator_username
        else:
            return None, None
