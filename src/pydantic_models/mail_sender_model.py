from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

from src.pydantic_models.common import NAME

USER_ID = Annotated[str, StringConstraints(min_length=1, max_length=26)]


class MailSenderModel(BaseModel):
    email: EmailStr
