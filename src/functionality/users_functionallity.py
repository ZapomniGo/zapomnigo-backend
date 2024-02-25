from typing import Dict, Any

from flask_bcrypt import generate_password_hash
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, aliased
from ulid import ULID

from src.database.models import Users, Sets, Flashcards, FoldersSets, Folders, Categories, Subcategories
from src.database.models.base import db
from src.database.repositories.sets_repository import SetsRepository
from src.database.repositories.users_repository import UsersRepository
from src.functionality.mailing_functionality import MailingFunctionality
from src.pydantic_models.users_models import UpdateUser, RegistrationModel


class UsersFunctionality:

    @staticmethod
    def create_user(json_data: RegistrationModel) -> Users:
        hashed_password = generate_password_hash(json_data.password).decode("utf-8")

        return Users(user_id=str(ULID()), username=json_data.username,
                     name=json_data.name, email=json_data.email,
                     password=hashed_password, age=json_data.age,
                     gender=json_data.gender,
                     privacy_policy=json_data.privacy_policy,
                     terms_and_conditions=json_data.terms_and_conditions,
                     marketing_consent=json_data.marketing_consent)

    @classmethod
    async def send_emails(cls, user: Users, user_update_fields: UpdateUser):
        """Send transactional email if the user has changed their email or password"""
        if not user.verified and user_update_fields.email:
            await MailingFunctionality.send_verification_email(user_update_fields.email, user.username,
                                                               verify_on_register=False)

        if user_update_fields.new_password and user_update_fields.password:
            await MailingFunctionality.send_reset_password_email(user.email, user.username, is_change_password=True)

    @classmethod
    def check_if_user_exists(cls, json_data) -> Users | None:
        email_or_username = json_data["email_or_username"]

        if user := UsersRepository.get_user_by_username(email_or_username):
            return user

        elif user := UsersRepository.get_user_by_email(email_or_username):
            return user

        return None

    @classmethod
    def export_user_data(cls, user: Users) -> Dict[str, Any]:
        user_sets: Result = db.session.execute(
            select(
                Sets, Flashcards
            )
            .join(Flashcards, Flashcards.set_id == Sets.set_id)
            .join(Categories, Categories.category_id == Sets.set_category, isouter=True)
            .join(Subcategories, Subcategories.subcategory_id == Sets.set_subcategory, isouter=True)
            .where(Sets.user_id == user.user_id))
        # sets_data = []
        # for row_sets in user_sets:
        #     sets_data.append({})

        # # Query for user's folders and related sets
        user_folders = db.session.execute(
            select(Folders, Sets).join(FoldersSets, FoldersSets.folder_id == Folders.folder_id).join(Sets,
                                                                                               FoldersSets.set_id == Sets.set_id).where(
                Folders.user_id == user.user_id))

        for row_folders in user_folders:
            print(f"{row_folders.Folders.folder_id}, {row_folders.Sets.set_name}")

        # Return the user's information, sets, and folders
        return {
            "user_info": {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "gender": user.gender,
                "age": user.age,
                "privacy_policy": user.privacy_policy,
                "terms_and_conditions": user.terms_and_conditions,
                "marketing_consent": user.marketing_consent
            },
            # "user_sets": sets_data,
            # "user_folders": folders_data
        }
