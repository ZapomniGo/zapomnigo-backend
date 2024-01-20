from pydantic import BaseModel, model_validator

from src.pydantic_models.common import PASSWORD


class ResetPasswordModel(BaseModel):
    token: str
    new_password: PASSWORD

    @model_validator(mode='before')
    def check_empty_token(cls, values):
        token = values.get('token')
        if not token or token == "":
            raise ValueError("Token field cannot be empty")
        return values
