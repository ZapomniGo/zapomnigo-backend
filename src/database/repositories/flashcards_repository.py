from datetime import datetime
from typing import List, Dict, Any

from src.database.models import Flashcards
from src.database.models.base import db


class FlashcardsRepository:
    @classmethod
    def get_flashcard_by_id(cls, flashcard_id: str) -> Flashcards | None:
        return db.session.query(Flashcards).filter_by(flashcard_id=flashcard_id).first()

    @classmethod
    def get_flashcards_by_set_id(cls, set_id: str) -> List[Flashcards]:
        return db.session.query(Flashcards).filter_by(set_id=set_id).all()

    @classmethod
    def edit_flashcard(cls, flashcard: Flashcards, json_data: Dict[str, Any]) -> None:
        flashcard.term = json_data.get("term", flashcard.term)
        flashcard.definition = json_data.get("definition", flashcard.definition)
        flashcard.notes = json_data.get("notes", flashcard.notes)
        db.session.commit()
