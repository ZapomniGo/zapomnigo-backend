from dataclasses import dataclass

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


@dataclass
class Folders(db.Model):
    folder_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    folder_modification_date: Mapped[str] = mapped_column(String(40), nullable=False)
    folder_title: Mapped[str] = mapped_column(String(40), nullable=False)
    folder_description: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.category_id"))

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="folders", cascade="all")
    categories: Mapped["Categories"] = relationship(back_populates="folders", cascade="all")
    folders_sets: Mapped["FoldersSets"] = relationship(back_populates="folders", cascade="all")
