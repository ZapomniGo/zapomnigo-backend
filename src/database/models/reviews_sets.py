from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class ReviewsSets(db.Model):
    review_set_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"))
    review_date: Mapped[str] = mapped_column(String(40), nullable=False)

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="reviews_sets", cascade="all")
    sets: Mapped["Sets"] = relationship(back_populates="reviews_sets", cascade="all")
