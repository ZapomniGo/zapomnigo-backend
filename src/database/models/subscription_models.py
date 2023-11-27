from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class SubscriptionModels(db.Model):
    subscription_model_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    subscription_model: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="subscription_models", cascade="all")
    organizations: Mapped["Organizations"] = relationship(back_populates="subscription_models", cascade="all")
