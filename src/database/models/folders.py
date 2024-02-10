from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.database.models.base import db


class Folders(db.Model):
    folder_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    folder_modification_date: Mapped[str] = mapped_column(String(40), nullable=False)
    folder_title: Mapped[str] = mapped_column(String(255), nullable=False)
    folder_description: Mapped[str] = mapped_column(String(4096), nullable=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.category_id"), nullable=True)
    subcategory_id: Mapped[str] = mapped_column(ForeignKey("subcategories.subcategory_id"), nullable=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.organization_id"), nullable=True)
    verified: Mapped[bool] = mapped_column(db.Boolean, nullable=True, default=False)

    # Creates a bidirectional relationship between tables
    users: Mapped[List["Users"]] = relationship(back_populates="folders")
    categories: Mapped[List["Categories"]] = relationship(back_populates="folders")
    subcategories: Mapped[List["Subcategories"]] = relationship(back_populates="folders")
    folders_sets: Mapped[List["FoldersSets"]] = relationship(back_populates="folders", cascade="all")
    organizations: Mapped[List["Organizations"]] = relationship(back_populates="folders")
