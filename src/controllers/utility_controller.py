from typing import Tuple, Dict, Any

from flask import request
from sqlalchemy import func, or_, desc

from src.config import ADMIN_USERNAME
from src.database.models import Sets, Folders, Flashcards
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
    def search(cls) -> Tuple[Dict[str, str], int]:
        search_terms = request.args.get("q")
        if not search_terms:
            return {"message": "No search query provided"}, 400

        query = db.session.query(Sets, Folders, Flashcards)
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