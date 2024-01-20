from typing import List, Dict, Any, Tuple

from flask_sqlalchemy.pagination import Pagination


class SetsFunctionality:
    @classmethod
    def display_sets_info(cls, result: Pagination | List[Tuple[...]], flashcards=None) -> List[Dict[str, Any]]:
        sets_list = []
        for row in result:
            set_dict = {
                'set_id': row.set_id,
                'set_name': row.set_name,
                'set_description': row.set_description,
                'set_modification_date': row.set_modification_date,
                'category_name': row.category_name,
                'organization_name': row.organization_name,
                'username': row.username,
            }
            sets_list.append(set_dict)

        if not flashcards:
            return sets_list

        flashcards_list = []
        for flashcard in flashcards:
            flashcard_dict = {
                'flashcard_id': flashcard.flashcard_id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'notes': flashcard.notes
            }
            flashcards_list.append(flashcard_dict)

        sets_list[0]["flashcards"] = flashcards_list

        return sets_list

    @classmethod
    def display_study_info(cls, flashcards: Pagination) -> List[Dict[str, Any]]:
        flashcards_list = []
        for flashcard in flashcards:
            flashcard_dict = {
                'flashcard_id': flashcard.flashcard_id,
                'term': flashcard.term,
                'definition': flashcard.definition,
                'confidence': flashcard.confidence
            }
            flashcards_list.append(flashcard_dict)

        return flashcards_list
