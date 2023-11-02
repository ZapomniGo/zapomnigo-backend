from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.models.base import db


@dataclass
class Organizations(db.Model):
    organization_id: Mapped[str] = mapped_column(String(26), primary_key=True)
    organization_name: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    organization_domain: Mapped[str] = mapped_column(String(40), nullable=False, unique=True)
    organization_creation_date:  Mapped[str] = mapped_column(String(40), nullable=False)
