from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class ResetPasswordModel(BaseModel):
    token: str
    new_password: Annotated[str, Field(min_length=8, max_length=80)]

    @model_validator(mode='before')
    def check_empty_token(cls, values):
        token = values.get('token')
        if not token or token == "":
            raise ValueError("Token field cannot be empty")
        return values