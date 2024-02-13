from typing import Tuple, Dict, Any

from flask import request
from sqlalchemy import func, or_, desc
from sqlalchemy.orm import joinedload

from src.config import ADMIN_USERNAME
from src.database.models import Sets, Folders, Flashcards, FoldersSets, Categories, Subcategories, Users
from src.database.models.base import db
from src.functionality.auth.auth_functionality import AuthFunctionality


class UtilityController:

    @staticmethod
    def get_health() -> Tuple[Dict[str, str], int]:
        return {"status": "healthy"}, 200

    @classmethod
    def check_user_access(cls, username: str) -> Tuple[Dict[str, Any], int] | None:
        """Returns a JSON Response if there is an error or the user doesn't have access"""
        logged_in_username = AuthFunctionality.get_session_username_or_user_id(request)
        if not logged_in_username:
            return {"message": "No username provided"}, 400

        if logged_in_username == ADMIN_USERNAME or logged_in_username == username:
            return None

        return {"message": "Admin privileges required."}, 403

    @classmethod
    def search(cls) -> Tuple[Dict[str, Any], int]:
        search_terms = request.args.get("q")
        if not search_terms:
            return {"message": "No search query provided"}, 400

        query = db.session.query(Sets, Folders, Flashcards)

        # Join statements based on your SQL join
        query = query.outerjoin(Flashcards, Sets.set_id == Flashcards.set_id)
        query = query.outerjoin(FoldersSets, Sets.set_id == FoldersSets.set_id)
        query = query.outerjoin(Folders, Folders.folder_id == FoldersSets.folder_id)

        # Use joinedload to eagerly load related entities
        query = query.options(
            joinedload(Sets.categories),
            joinedload(Sets.subcategories),
            joinedload(Sets.users),
            joinedload(Folders.categories),
            joinedload(Folders.subcategories),
            joinedload(Folders.users)
        )

        query = query.add_columns(
            func.ts_rank(
                func.to_tsvector('simple', Sets.set_name + ' ' + Sets.set_description),
                func.plainto_tsquery('simple', search_terms)
            ).label('rank_sets'),
            func.ts_rank(
                func.to_tsvector('simple', Folders.folder_title + ' ' + Folders.folder_description),
                func.plainto_tsquery('simple', search_terms)
            ).label('rank_folders'),
            func.ts_rank(
                func.to_tsvector('simple', Flashcards.term + ' ' + Flashcards.definition),
                func.plainto_tsquery('simple', search_terms)
            ).label('rank_flashcards')
        )

        query = query.filter(
            or_(
                func.to_tsvector('simple', Sets.set_name + ' ' + Sets.set_description).match(search_terms),
                func.to_tsvector('simple', Folders.folder_title + ' ' + Folders.folder_description).match(search_terms),
                func.to_tsvector('simple', Flashcards.term + ' ' + Flashcards.definition).match(search_terms)
            )
        )

        results = query.order_by(desc('rank_sets'), desc('rank_folders'), desc('rank_flashcards')).all()

        formatted_results = {"sets": [], "folders": [], "flashcards": []}
        unique_set_ids = set()  # To track unique set_ids
        unique_folder_ids = set()  # To track unique folder_ids

        for result in results:
            sets_instance, folders_instance, flashcards_instance, rank_sets, rank_folders, rank_flashcards = result

            # Format the results for each entity type
            formatted_sets = {
                'set_id': sets_instance.set_id,
                'set_name': sets_instance.set_name,
                'set_description': sets_instance.set_description,
                'set_modification_date': sets_instance.set_modification_date,
                'category_name': sets_instance.categories.category_name if sets_instance.categories else None,
                'subcategory_name': sets_instance.subcategories.subcategory_name if sets_instance.subcategories else None,
                'username': sets_instance.users.username if sets_instance.users else None,
                'verified': sets_instance.verified,
                'rank': rank_sets
            } if sets_instance and sets_instance.set_id not in unique_set_ids else None

            formatted_folders = {
                'folder_id': folders_instance.folder_id,
                'folder_title': folders_instance.folder_title,
                'folder_description': folders_instance.folder_description,
                'folder_modification_date': folders_instance.folder_modification_date,
                'category_name': folders_instance.categories.category_name if folders_instance.categories else None,
                'subcategory_name': folders_instance.subcategories.subcategory_name if folders_instance.subcategories else None,
                'username': folders_instance.users.username if folders_instance.users else None,
                'verified': folders_instance.verified,
                'rank': rank_folders
            } if folders_instance and folders_instance.folder_id not in unique_folder_ids else None

            if formatted_sets:
                formatted_results["sets"].append(formatted_sets)
                unique_set_ids.add(sets_instance.set_id)

            if formatted_folders:
                formatted_results["folders"].append(formatted_folders)
                unique_folder_ids.add(folders_instance.folder_id)

        return {"results": formatted_results}, 200
