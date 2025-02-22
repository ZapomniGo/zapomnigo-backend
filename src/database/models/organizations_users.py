from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import db


class OrganizationsUsers(db.Model):
    organization_user_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.organization_id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))

    # Creates a bidirectional relationship between tables
    users: Mapped["Users"] = relationship(back_populates="organizations_users", cascade="all")
    organizations: Mapped["Organizations"] = relationship(back_populates="organizations_users", cascade="all")

    # Make the combination of organization_id and user_id unique
    __table_args__ = (UniqueConstraint("organization_id", "user_id"),)
