from sqlalchemy.orm import mapped_column, Mapped

from src.database.models.base import db


class Users(db.Model):

    user_id: Mapped[str] = mapped_column(db.String(26), primary_key=True)
    username: Mapped[str] = mapped_column(db.String(40), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(nullable=True)
    creation_date: Mapped[str] = mapped_column(db.String(40), nullable=False)
    gender: Mapped[str] = mapped_column(db.String(1), nullable=True)
    verified: Mapped[bool] = mapped_column(db.Boolean, default=False)
    subscription_date: Mapped[str] = mapped_column(db.String(40), nullable=False)

