from dataclasses import dataclass

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


@dataclass
class OrganizationsUsers:
    organization_user_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.organization_id"))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    users: Mapped["Users"] = relationship(back_populates="organizations_users", cascade="all")
    organizations: Mapped["Organizations"] = relationship(back_populates="organizations_users", cascade="all")
    __table_args = (UniqueConstraint("organization_id","user_id"))