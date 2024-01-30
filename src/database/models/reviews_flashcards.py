from typing import List

from sqlalchemy import String, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class ReviewsFlashcards(db.Model):
    reviews_flashcards_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    flashcard_id: Mapped[str] = mapped_column(ForeignKey("flashcards.flashcard_id"))
    confidence: Mapped[int] = mapped_column(Integer, nullable=False)

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="reviews_flashcards")
    flashcards: Mapped[List["Flashcards"]] = relationship(back_populates="reviews_flashcards")

    __table_args__ = (UniqueConstraint("user_id", "flashcard_id", name="user_id_flashcard_id_unique"),)
