from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Flashcards(db.Model):
    flashcard_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    term: Mapped[str] = mapped_column(String(524288), nullable=False)
    definition: Mapped[str] = mapped_column(String(524288), nullable=False)
    notes: Mapped[str] = mapped_column(String(524288), nullable=True)
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"), nullable=False)
    flashcard_creation_time: Mapped[str] = mapped_column(String(40), nullable=True)

    # Creates a bidirectional relationship between tables
    sets: Mapped["Sets"] = relationship(back_populates="flashcards")
    liked_flashcards: Mapped[List["LikedFlashcards"]] = relationship(back_populates="flashcards", cascade="all")
    reviews_flashcards: Mapped[List["ReviewsFlashcards"]] = relationship(back_populates="flashcards", cascade="all")

    def to_json(self):
        return {"flashcard_id": self.flashcard_id,
                "term": self.term,
                "definition": self.definition,
                "notes": self.notes,
                }

    def single_to_json(self):
        return {"flashcard_id": self.flashcard_id,
                "set_id": self.set_id,
                "term": self.term,
                "definition": self.definition,
                "notes": self.notes,
                }
