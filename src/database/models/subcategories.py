from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class Subcategories(db.Model):
    subcategory_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    subcategory_name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)

    # Creates a bidirectional relationship between tables
    sets: Mapped["Sets"] = relationship(back_populates="subcategories")
    folders: Mapped["Folders"] = relationship(back_populates="subcategories")
    category_subcategories: Mapped["CategorySubcategories"] = relationship(back_populates="subcategories")

    def to_json(self):
        return {"subcategory_id": self.subcategory_id,
                "subcategory_name": self.category_name}