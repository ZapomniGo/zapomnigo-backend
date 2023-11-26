from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Flashcards(db.Model):
    flashcard_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    term: Mapped[str] = mapped_column(String(40), nullable=True)
    definition: Mapped[str] = mapped_column(String(255), nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"))

    # Creates a bidirectional relationship between tables
    sets: Mapped["Sets"] = relationship(back_populates="flashcards", cascade="all")
    liked_flashcards: Mapped["LikedFlashcards"] = relationship(back_populates="flashcards", cascade="all")
    reviews_flashcards: Mapped["ReviewsFlashcards"] = relationship(back_populates="flashcards", cascade="all")
