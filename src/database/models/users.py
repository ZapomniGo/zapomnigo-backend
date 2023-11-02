from dataclasses import dataclass

from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


@dataclass
class Users(db.Model):
    user_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    user_creation_date: Mapped[str] = mapped_column(String(40), nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    subscription_date: Mapped[str] = mapped_column(String(40), nullable=False)
    subscription_model_id: Mapped[str] = mapped_column(ForeignKey("subscription_models.subscription_model_id"))

    # Creates a bidirectional relationship between tables
    subscription_models: Mapped["SubscriptionModels"] = relationship(back_populates="users", cascade="all")
    organizations_users: Mapped["OrganizationsUsers"] = relationship(back_populates="users", cascade="all")
    sets: Mapped["Sets"] = relationship(back_populates="users", cascade="all")
    comments: Mapped["Comments"] = relationship(back_populates="users", cascade="all")
    folders: Mapped["Folders"] = relationship(back_populates="users", cascade="all")
    preferences: Mapped["Preferences"] = relationship(back_populates="users", cascade="all")
    flashcards: Mapped["Flashcards"] = relationship(back_populates="users", cascade="all")
    liked_sets: Mapped["LikedSets"] = relationship(back_populates="users", cascade="all")
    reviews_sets: Mapped["ReviewsSets"] = relationship(back_populates="users", cascade="all")
    liked_flashcards: Mapped["LikedFlashcards"] = relationship(back_populates="users", cascade="all")