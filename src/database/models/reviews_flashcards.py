from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class ReviewsFlashcards(db.Model):
    liked_flashcard_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"))
    flashcard_id: Mapped[str] = mapped_column(ForeignKey("flashcards.flashcard_id"))
    confidence: Mapped[int] = mapped_column(Integer, nullable=True)

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="reviews_flashcards", cascade="all")
    sets: Mapped["Sets"] = relationship(back_populates="reviews_flashcards", cascade="all")
    flashcards: Mapped["Flashcards"] = relationship(back_populates="reviews_flashcards", cascade="all")
