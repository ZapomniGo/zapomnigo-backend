import string
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.pydantic_models.common import NAME, PASSWORD, ID


class RegistrationModel(BaseModel):
    name: NAME
    username: NAME
    email: EmailStr
    password: PASSWORD
    age: int = Field(..., gt=5, le=99)
    gender: Literal["M", "F", "O"]
    organization: Optional[ID] = None
    privacy_policy: bool
    terms_and_conditions: bool
    marketing_consent: bool

    @field_validator("password")
    def validate_password(cls, value):
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        if not any(c in string.punctuation for c in value):
            raise ValueError("Password must contain at least one special character")

        return value


class LoginModel(BaseModel):
    email_or_username: str
    password: str


class ResetPasswordModel(BaseModel):
    token: str
    new_password: PASSWORD

    @field_validator("token", mode='before')
    def check_empty_token(cls, values):
        if not values or values == "":
            raise ValueError("Token field cannot be empty")
        return values
