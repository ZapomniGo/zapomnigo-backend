from typing import Tuple, Dict, Any

from flask import request
from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import func, or_, desc, and_
from sqlalchemy.orm import joinedload

from src.config import ADMIN_USERNAME
from src.database.models import Sets, Folders, Flashcards, FoldersSets, Categories, Subcategories, Users
from src.database.models.base import db
from src.database.repositories.folders_repository import FoldersRepository
from src.database.repositories.sets_repository import SetsRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.common import CommonFunctionality


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

        page, size, _, _ = CommonFunctionality.get_pagination_params(request)

        sets_results = SetsRepository.search_sets_flashcards(search_terms, page, size)
        folders_results = FoldersRepository.search_folders(search_terms, page, size)

        formatted_results = CommonFunctionality.search_format_results(folders_results, sets_results)

        return {"results": formatted_results}, 200
