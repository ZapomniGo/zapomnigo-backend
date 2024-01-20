from typing import List, Any

from pydantic import BaseModel

from src.database.models.base import db
from src.utilities.parsers import filter_none_values


class CommonRepository:

    @classmethod
    def add_many_objects_to_db(cls, objects: List[Any]) -> None:
        db.session.add_all(objects)
        db.session.commit()

    @classmethod
    def add_object_to_db(cls, obj) -> None:
        db.session.add(obj)
        db.session.commit()

    @classmethod
    def get_all_objects_from_db(cls, obj):
        return db.session.query(obj).all()

    @classmethod
    def delete_object_from_db(cls, obj) -> None:
        db.session.delete(obj)
        db.session.commit()

    @classmethod
    def edit_object(cls, obj, json_data: BaseModel) -> None:
        for field_name, value in filter_none_values(json_data).items():
            setattr(obj, field_name, value)

        db.session.commit()
