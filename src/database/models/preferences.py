from sqlalchemy import String, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class Preferences(db.Model):
    preferences_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    min_flashcards_to_show: Mapped[int] = mapped_column(Integer, nullable=True)
    max_flashcards_to_show: Mapped[int] = mapped_column(Integer, nullable=True)
    prompt_with: Mapped[str] = mapped_column(String(40), nullable=True)

    # Make user_id unique
    __table_args__ = (UniqueConstraint("user_id"),)

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="preferences", cascade="all")
