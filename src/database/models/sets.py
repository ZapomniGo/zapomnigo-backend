from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Sets(db.Model):
    set_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    set_name: Mapped[str] = mapped_column(String(255), nullable=False)
    set_description: Mapped[str] = mapped_column(String(4096), nullable=True)
    set_modification_date: Mapped[str] = mapped_column(String(40), nullable=False)
    set_category: Mapped[str] = mapped_column(ForeignKey("categories.category_id"), nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.organization_id"), nullable=True)

    # Creates a bidirectional relationship between tables
    users: Mapped[List["Users"]] = relationship(back_populates="sets")
    categories: Mapped[List["Categories"]] = relationship(back_populates="sets")
    comments: Mapped[List["Comments"]] = relationship(back_populates="sets", cascade="all")
    folders_sets: Mapped[List["FoldersSets"]] = relationship(back_populates="sets", cascade="all")
    flashcards: Mapped[List["Flashcards"]] = relationship(back_populates="sets", cascade="all")
    liked_sets: Mapped[List["LikedSets"]] = relationship(back_populates="sets", cascade="all")
    reviews_sets: Mapped[List["ReviewsSets"]] = relationship(back_populates="sets", cascade="all")
    liked_flashcards: Mapped[List["LikedFlashcards"]] = relationship(back_populates="sets", cascade="all")
    reviews_flashcards: Mapped[List["ReviewsFlashcards"]] = relationship(back_populates="sets", cascade="all")
    organizations: Mapped[List["Organizations"]] = relationship(back_populates="sets")

    def get_user_id(self):
        return self.user_id

    def to_json(self, username, flashcards):
        return {"set_id": self.set_id,
                "set_name": self.set_name,
                "set_description": self.set_description,
                "set_modification_date": self.set_modification_date,
                "set_category": self.set_category,
                "username": username,
                "organization": self.organization_id,
                "flashcards": flashcards
                }
