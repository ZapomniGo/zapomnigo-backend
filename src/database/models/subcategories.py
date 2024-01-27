from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class Subcategories(db.Model):
    subcategory_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    subcategory_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    category_id: Mapped[str] = mapped_column(String(26), ForeignKey('categories.category_id'), nullable=True)

    # Creates a bidirectional relationship between tables
    sets: Mapped["Sets"] = relationship(back_populates="subcategories")
    folders: Mapped["Folders"] = relationship(back_populates="subcategories")
    categories: Mapped["Categories"] = relationship(back_populates="subcategories")