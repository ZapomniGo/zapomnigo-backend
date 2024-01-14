from datetime import datetime
from typing import List, Dict, Any

from flask_sqlalchemy.pagination import Pagination
from sqlalchemy import delete

from src.database.models import Flashcards, ReviewsFlashcards
from src.database.models.base import db


class FlashcardsRepository:
    @classmethod
    def get_flashcard_by_id(cls, flashcard_id: str) -> Flashcards | None:
        return db.session.query(Flashcards).filter_by(flashcard_id=flashcard_id).first()

    @classmethod
    def get_flashcards_by_set_id(cls, set_id: str) -> List[Flashcards]:
        return db.session.query(Flashcards).filter_by(set_id=set_id).all()

    @classmethod
    def paginate_flashcards_for_set(cls, set_id: str, page: int = 1,
                                    size: int = 20, user_id: str = None, is_study=False) -> Pagination:
        if not is_study:
            return db.session.query(Flashcards).filter_by(set_id=set_id).paginate(page=page, per_page=size,
                                                                                  error_out=True)

        return db.session.query(
            Flashcards.flashcard_id,
            Flashcards.term,
            Flashcards.definition,
            ReviewsFlashcards.confidence
        ).outerjoin(
            ReviewsFlashcards,
            (Flashcards.flashcard_id == ReviewsFlashcards.flashcard_id) &
            (ReviewsFlashcards.user_id == user_id)
        ).filter(
            Flashcards.set_id == set_id
        ).paginate(page=page, per_page=size,
                   error_out=True)

    @classmethod
    def edit_flashcard(cls, flashcard: Flashcards, json_data: Dict[str, Any]) -> None:
        flashcard.term = json_data.get("term", flashcard.term)
        flashcard.definition = json_data.get("definition", flashcard.definition)
        flashcard.notes = json_data.get("notes", flashcard.notes)
        db.session.commit()

    @classmethod
    def delete_flashcards_by_set_id(cls, set_id: str) -> None:
        db.session.execute(delete(Flashcards).where(Flashcards.set_id == set_id))
        db.session.commit()
