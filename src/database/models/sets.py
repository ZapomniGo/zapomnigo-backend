from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Sets(db.Model):
    set_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    set_name: Mapped[str] = mapped_column(String(40), nullable=False)
    set_description: Mapped[str] = mapped_column(String(255), nullable=True)
    set_modification_date: Mapped[str] = mapped_column(String(40), nullable=False)
    set_category: Mapped[str] = mapped_column(ForeignKey("categories.category_id"), nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="sets", cascade="all")
    categories: Mapped["Categories"] = relationship(back_populates="sets", cascade="all")
    comments: Mapped["Comments"] = relationship(back_populates="sets", cascade="all")
    folders_sets: Mapped["FoldersSets"] = relationship(back_populates="sets", cascade="all")
    flashcards: Mapped["Flashcards"] = relationship(back_populates="sets", cascade="all")
    liked_sets: Mapped["LikedSets"] = relationship(back_populates="sets", cascade="all")
    reviews_sets: Mapped["ReviewsSets"] = relationship(back_populates="sets", cascade="all")
    liked_flashcards: Mapped["LikedFlashcards"] = relationship(back_populates="sets", cascade="all")
    reviews_flashcards: Mapped["ReviewsFlashcards"] = relationship(back_populates="sets", cascade="all")
