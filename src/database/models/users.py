from typing import List

from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Users(db.Model):
    user_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_photo: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=True)
    role: Mapped[str] = mapped_column(String(40), nullable=True)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    # subscription_date: Mapped[str] = mapped_column(String(40), nullable=True)
    privacy_policy: Mapped[bool] = mapped_column(Boolean, nullable=False)
    terms_and_conditions: Mapped[bool] = mapped_column(Boolean, nullable=False)
    marketing_consent: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # subscription_model_id: Mapped[str] = mapped_column(ForeignKey("subscription_models.subscription_model_id"))

    # Creates a bidirectional relationship between tables
    # subscription_models: Mapped["SubscriptionModels"] = relationship(back_populates="users", cascade="all")
    organizations_users: Mapped["OrganizationsUsers"] = relationship(back_populates="users", cascade="all")
    sets: Mapped[List["Sets"]] = relationship(back_populates="users", cascade="all")
    comments: Mapped["Comments"] = relationship(back_populates="users", cascade="all")
    folders: Mapped[List["Folders"]] = relationship(back_populates="users", cascade="all")
    preferences: Mapped["Preferences"] = relationship(back_populates="users", cascade="all")
    liked_sets: Mapped["LikedSets"] = relationship(back_populates="users", cascade="all")
    reviews_sets: Mapped[List["ReviewsSets"]] = relationship(back_populates="users", cascade='all')
    liked_flashcards: Mapped["LikedFlashcards"] = relationship(back_populates="users", cascade="all")
    reviews_flashcards: Mapped[List["ReviewsFlashcards"]] = relationship(back_populates="users", cascade="all")
