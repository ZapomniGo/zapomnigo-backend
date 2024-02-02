from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class CategorySubcategories(db.Model):
    category_subcategories_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    category_id: Mapped[str] = mapped_column(String(26), ForeignKey("categories.category_id"), nullable=False)
    subcategory_id: Mapped[str] = mapped_column(String(26), ForeignKey("subcategories.subcategory_id"), nullable=False)
    order: Mapped[int] = mapped_column(db.Integer, nullable=True)

    # Creates a bidirectional relationship between tables
    categories: Mapped["Categories"] = relationship(back_populates="category_subcategories")
    subcategories: Mapped["Subcategories"] = relationship(back_populates="category_subcategories")

    __table_args__ = (UniqueConstraint("category_id", "subcategory_id", name="category_subcategory_unique"),)
