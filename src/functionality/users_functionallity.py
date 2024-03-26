from collections import defaultdict
from typing import Dict, Any, List

from flask_bcrypt import generate_password_hash
from ulid import ULID

from src.database.models import Users
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
                     role=json_data.role,
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
        user_sets = UsersRepository.get_user_sets(user.user_id)
        user_folders = UsersRepository.get_user_folders(user.user_id)

        sets_data = cls.display_user_sets(user_sets)
        folders_data = cls.display_user_folders(user_folders)

        return {
            "user_info": {
                "username": user.username,
                "name": user.name,
                "email": user.email,
                "gender": user.gender,
                "age": user.age,
                "role": user.role,
                "privacy_policy": user.privacy_policy,
                "terms_and_conditions": user.terms_and_conditions,
                "marketing_consent": user.marketing_consent
            },
            "user_sets": sets_data,
            "user_folders": list(folders_data.values())
        }

    @classmethod
    def display_user_folders(cls, user_folders):
        folders_data = defaultdict(lambda: defaultdict(list))
        for row_folders in user_folders:
            folder_id = row_folders.Folders.folder_id
            folders_data[folder_id]["folder_id"] = folder_id
            folders_data[folder_id]["folder_title"] = row_folders.Folders.folder_title
            folders_data[folder_id]["folder_description"] = row_folders.Folders.folder_description
            folders_data[folder_id][
                "category"] = row_folders.Categories.category_name if row_folders.Categories else None
            folders_data[folder_id][
                "subcategory"] = row_folders.Subcategories.subcategory_name if row_folders.Subcategories else None
            folders_data[folder_id]["sets"].append({
                "set_id": row_folders.Sets.set_id,
                "set_name": row_folders.Sets.set_name,
                "set_description": row_folders.Sets.set_description
            })

        # Convert defaultdict to regular dict for JSON serialization
        folders_data = {k: dict(v) for k, v in folders_data.items()}
        return folders_data

    @classmethod
    def display_user_sets(cls, user_sets) -> List[Dict[str, Any]]:
        sets_data = []
        for row_sets in user_sets:
            sets_data.append({"set_id": row_sets.Sets.set_id,
                              "set_name": row_sets.Sets.set_name,
                              "set_description": row_sets.Sets.set_description,
                              "category": row_sets.Categories.category_name if row_sets.Categories else None,
                              "subcategory": row_sets.Subcategories.subcategory_name if row_sets.Subcategories else None,
                              "flashcards": [{"flashcard_id": row_flashcards.flashcard_id,
                                              "term": row_flashcards.term,
                                              "definition": row_flashcards.definition,
                                              "notes": row_flashcards.notes} for row_flashcards in
                                             row_sets.Sets.flashcards]})

        return sets_data
