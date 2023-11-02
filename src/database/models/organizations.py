from dataclasses import dataclass

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db
from src.database.models import SubscriptionModels


@dataclass
class Organizations(db.Model):
    organization_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    organization_domain: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    organization_creation_date: Mapped[str] = mapped_column(String(40), nullable=False)
    subscription_model_id: Mapped[str] = mapped_column(ForeignKey("subscription_models.subscription_model_id"))
    subscription_model: Mapped["SubscriptionModels"] = relationship(back_populates="organizations")
