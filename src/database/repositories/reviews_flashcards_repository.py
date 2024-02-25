from sqlalchemy import and_

from src.database.models import ReviewsFlashcards
from src.database.models.base import db
from src.pydantic_models.flashcards_model import StudyFlashcardsModel


class ReviewsFlashcardsRepository:
    @classmethod
    def get_review_by_flashcard_id(cls, flashcard_id: str, user_id: str) -> ReviewsFlashcards | None:
        return db.session.query(ReviewsFlashcards).filter(
            and_(
                ReviewsFlashcards.flashcard_id == flashcard_id,
                ReviewsFlashcards.user_id == user_id
            )
        ).first()

    @classmethod
    def edit_review_flashcard(cls, set_obj: ReviewsFlashcards, json_data: StudyFlashcardsModel) -> None:
        if json_data.correctness == 0:
            set_obj.confidence -= 1
        else:
            set_obj.confidence += 1
