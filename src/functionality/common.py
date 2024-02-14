from typing import List, Tuple, Dict, Any

from flask import Request
from flask_sqlalchemy.pagination import Pagination

from src.utilities.parsers import arg_to_bool


class CommonFunctionality:
    @classmethod
    def get_pagination_params(cls, request: Request) -> tuple[int, int, bool, bool]:
        page = request.args.get('page', type=int)
        size = request.args.get('size', type=int)
        sort_by_date = request.args.get('sort_by_date', type=str, default='true')
        ascending = request.args.get('ascending', type=str, default='false')
        sort_by_date = arg_to_bool(sort_by_date)
        ascending = arg_to_bool(ascending)
        return page, size, sort_by_date, ascending

    @classmethod
    def search_format_results(cls, folders_results: Pagination | List[Tuple[...]],
                              sets_results: Pagination | List[Tuple[...]]) -> Dict[str, List[Dict[str, Any]]]:

        formatted_results = {"sets": [], "folders": []}
        unique_entities = {"sets": set(), "folders": set()}
        for result in sets_results:
            sets_instance, flashcards_instance, rank_sets, rank_flashcards = result
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
            } if sets_instance and sets_instance.set_id not in unique_entities["sets"] else None

            if formatted_sets:
                formatted_results["sets"].append(formatted_sets)
                unique_entities["sets"].add(sets_instance.set_id)

        for result in folders_results:
            folders_instance, rank_folders = result
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
            } if folders_instance and folders_instance.folder_id not in unique_entities["folders"] else None

            if formatted_folders:
                formatted_results["folders"].append(formatted_folders)
                unique_entities["folders"].add(folders_instance.folder_id)

        return formatted_results
