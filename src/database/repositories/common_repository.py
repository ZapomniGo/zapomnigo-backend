from typing import List, Any

from src.database.models.base import db


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
