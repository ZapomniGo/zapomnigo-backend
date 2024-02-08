from datetime import datetime
from typing import List, Dict, Any, Tuple

from flask_sqlalchemy.pagination import Pagination
from lxml.html import clean
from ulid import ULID

from src.database.models import Flashcards, Sets
from src.pydantic_models.sets_model import SetsModel


class SetsFunctionality:

    @classmethod
    def create_set(cls, json_data: SetsModel, user_id: str) -> Sets:
        return Sets(set_id=str(ULID()), set_name=json_data.set_name,
                    set_description=json_data.set_description,
                    set_modification_date=str(datetime.now()),
                    set_category=json_data.set_category,
                    set_subcategory=json_data.set_subcategory,
                    user_id=user_id,
                    organization_id=json_data.organization_id)

    @classmethod
    def sanitize_html(cls, html):
        cleaner = clean.Cleaner()

        cleaner.allow_tags = ['p', 'span', 'math', 'semantics', 'mrow', 'mi', 'mo', 'msup', 'mn', 'annotation', 'img']
        cleaner.remove_unknown_tags = False

        # Don't remove these attributes:
        cleaner.safe_attrs = clean.defs.safe_attrs | {'class', 'data-value', 'contenteditable', 'aria-hidden', 'style',
                                                      'xmlns', 'encoding', 'src'}
        return cleaner.clean_html(html)

    @classmethod
    def create_flashcards(cls, json_data: SetsModel, set_id: str):
        flashcards_objects = []
        for flashcard in json_data.flashcards:
            flashcard.term = cls.sanitize_html(flashcard.term)
            flashcard.definition = cls.sanitize_html(flashcard.definition)
            flashcards_objects.append(Flashcards(flashcard_id=str(ULID()), term=flashcard.term,
                                                 definition=flashcard.definition,
                                                 notes=flashcard.notes,
                                                 set_id=set_id, flashcard_creation_time=str(datetime.now())))
        return flashcards_objects

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
                "subcategory_name": row.subcategory_name,
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
                'notes': flashcard.notes,
                "flashcard_creation_time": flashcard.flashcard_creation_time
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
