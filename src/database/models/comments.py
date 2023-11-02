from dataclasses import dataclass

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


@dataclass
class Comments(db.Model):
    comment_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    comment: Mapped[str] = mapped_column(String(255), primary_key=True)
    comment_creation_date: Mapped[str] = mapped_column(String(40), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"))

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="comments", cascade="all")
    sets: Mapped["Sets"] = relationship(back_populates="comments", cascade="all")
