from dataclasses import dataclass

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


@dataclass
class FoldersSets(db.Model):
    folder_set_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    folder_id: Mapped[str] = mapped_column(ForeignKey("folders.folder_id"))
    set_id: Mapped[str] = mapped_column(ForeignKey("sets.set_id"))

    # Creates a bidirectional relationship between tables
    folders: Mapped["Folders"] = relationship(back_populates="folders_sets", cascade="all")
    sets: Mapped["Sets"] = relationship(back_populates="folders_sets", cascade="all")

    # Make the combination of organization_id and user_id unique
    __table_args__ = (UniqueConstraint("folder_id", "set_id"),)
