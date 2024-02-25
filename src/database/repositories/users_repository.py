from flask_bcrypt import generate_password_hash

from src.database.models import Users
from src.database.models.base import db


class UsersRepository:

    @classmethod
    def get_user_by_ulid(cls, user_id: str) -> Users | None:
        return db.session.query(Users).filter_by(user_id=user_id).first()

    @classmethod
    def get_user_by_username(cls, username: str) -> Users | None:
        return db.session.query(Users).filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email: str) -> Users | None:
        return db.session.query(Users).filter_by(email=email).first()

    @classmethod
    def change_verified_status(cls, user: Users, verified: bool) -> None:
        user.verified = verified

    @classmethod
    def reset_password(cls, user: Users, new_password: str) -> None:
        hashed_password = generate_password_hash(new_password).decode("utf-8")
        user.password = hashed_password
