from src.database.models import Users
from src.database.models.base import db


class UsersRepository:

    @classmethod
    def get_user_by_username(cls, username: str) -> Users | None:
        return db.session.query(Users).filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: str) -> Users | None:
        return db.session.query(Users).filter_by(email=email).first()
