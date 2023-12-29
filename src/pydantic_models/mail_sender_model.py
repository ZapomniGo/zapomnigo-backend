from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

from src.pydantic_models.common import NAME

USER_ID = Annotated[str, StringConstraints(min_length=1, max_length=26)]


class MailSenderModel(BaseModel):
    user_id: USER_ID  # type: ignore
    username: NAME  # type: ignore
    email: EmailStr
