from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class Organizations(db.Model):
    organization_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    organization_domain: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    subscription_model_id: Mapped[str] = mapped_column(ForeignKey("subscription_models.subscription_model_id"))

    # Creates a bidirectional relationship between tables
    subscription_models: Mapped["SubscriptionModels"] = relationship(back_populates="organizations")
    organizations_users: Mapped["OrganizationsUsers"] = relationship(back_populates="organizations",
                                                                     cascade="all")

    def to_json(self):
        return {"organization_id": self.organization_id,
                "organization_name": self.organization_name,
                "organization_domain": self.organization_domain,
                "subscription_model_id": self.subscription_model_id}
