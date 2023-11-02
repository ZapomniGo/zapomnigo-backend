from dataclasses import dataclass

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


@dataclass
class Sets(db.Model):
    set_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    set_name: Mapped[str] = mapped_column(String(40), nullable=False)
    set_description: Mapped[str] = mapped_column(String(255), nullable=True)
    set_creation_date: Mapped[str] = mapped_column(String(40), nullable=False)
    set_modification_date: Mapped[str] = mapped_column(String(40), nullable=False)
    set_category: Mapped[str] = mapped_column(ForeignKey("categories.category_id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="sets", cascade="all")
    categories: Mapped["Categories"] = relationship(back_populates="sets", cascade="all")
    sets: Mapped["Comments"] = relationship(back_populates="sets", cascade="all")
    folders_sets: Mapped["FoldersSets"] = relationship(back_populates="sets", cascade="all")