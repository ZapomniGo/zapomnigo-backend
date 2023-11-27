from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Comments(db.Model):
    comment_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    comment: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"))

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="comments", cascade="all")
    sets: Mapped["Sets"] = relationship(back_populates="comments", cascade="all")
