from typing import Tuple, Dict, Any

from flask import request

from src.config import ADMIN_USERNAME
from src.database.repositories.folders_repository import FoldersRepository
from src.database.repositories.sets_repository import SetsRepository
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.functionality.common import CommonFunctionality
from src.utilities.parsers import arg_to_bool


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

        sets_page_number = request.args.get("sets_page_number", type=int)
        sets_page_size = request.args.get("sets_page_size", type=int)
        folders_page_number = request.args.get("folders_page_number", type=int)
        folders_page_size = request.args.get("folders_page_size", type=int)
        category_id = request.args.get('category_id', type=str)
        subcategory_id = request.args.get('subcategory_id', type=str)

        sets_results = SetsRepository.search_sets_flashcards(search_terms, sets_page_number, sets_page_size,
                                                             category_id, subcategory_id)
        folders_results = FoldersRepository.search_folders(search_terms, folders_page_number, folders_page_size,
                                                           category_id, subcategory_id)

        formatted_results = CommonFunctionality.search_format_results(folders_results, sets_results,
                                                                      main_page_search=True)

        return {"results": formatted_results}, 200
