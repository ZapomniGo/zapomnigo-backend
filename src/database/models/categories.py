from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class Categories(db.Model):
    category_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    category_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

    # Creates a bidirectional relationship between tables
    sets: Mapped["Sets"] = relationship(back_populates="categories")
    folders: Mapped["Folders"] = relationship(back_populates="categories")
    subcategories: Mapped["Subcategories"] = relationship(back_populates="categories")

    def to_json(self):
        return {"category_id": self.category_id,
                "category_name": self.category_name}
