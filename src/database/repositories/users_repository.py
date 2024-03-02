from flask_bcrypt import generate_password_hash
from sqlalchemy import select, Result

from src.database.models import Users, Sets, Flashcards, FoldersSets, Folders, Categories, Subcategories
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

    @classmethod
    def get_user_sets(cls, user_id: str) -> Result:
        user_sets: Result = db.session.execute(
            select(
                Sets, Flashcards, Categories, Subcategories
            )
            .join(Flashcards, Flashcards.set_id == Sets.set_id)
            .join(Categories, Categories.category_id == Sets.set_category, isouter=True)
            .join(Subcategories, Subcategories.subcategory_id == Sets.set_subcategory, isouter=True)
            .where(Sets.user_id == user_id))

        return user_sets

    @classmethod
    def get_user_folders(cls, user_id: str) -> Result:
        user_folders: Result = db.session.execute(
            select(FoldersSets, Folders, Categories, Subcategories, Sets).distinct()
            .join(Folders, Folders.folder_id == FoldersSets.folder_id)
            .join(Sets, (Sets.set_id == FoldersSets.set_id) & (Sets.user_id == Folders.user_id))
            .join(Categories, Categories.category_id == Folders.category_id, isouter=True)
            .join(Subcategories, Subcategories.subcategory_id == Folders.subcategory_id, isouter=True)
            .where(Folders.user_id == user_id))

        return user_folders
