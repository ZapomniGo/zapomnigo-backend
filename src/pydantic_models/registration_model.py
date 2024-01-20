import string
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.pydantic_models.common import NAME, PASSWORD


class RegistrationModel(BaseModel):
    name: NAME
    username: NAME
    email: EmailStr
    password: PASSWORD
    age: int = Field(..., gt=5, le=99)
    gender: Literal["M", "F", "O"]
    organization: Optional[str] = None
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
