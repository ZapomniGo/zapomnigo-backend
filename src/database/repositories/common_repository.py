from src.database.models.base import db


class CommonRepository:
    @classmethod
    def add_object_to_db(cls, obj):
        db.session.add(obj)
        db.session.commit()
