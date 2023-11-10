import string
from typing import Annotated, Literal

from pydantic import BaseModel, StringConstraints, EmailStr, Field, field_validator


class RegistrationModel(BaseModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=40)]  # type: ignore
    username: Annotated[str, StringConstraints(min_length=2, max_length=40)]  # type: ignore
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=80)]
    age: int = Field(..., gt=5, le=99)
    gender: Literal["M", "F", "O"]
    subscription_model: Literal["6 months", "1 month", "1 year"]
    privacy_policy: bool
    terms_and_conditions: bool
    marketing_consent: bool

    @field_validator("password")
    @classmethod
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
