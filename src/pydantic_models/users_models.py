import string
from typing import Literal, Optional, Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.pydantic_models.common import NAME, PASSWORD, ID, AGE

USER_ROLES = Literal["Student", "Parent", "Teacher"]

class RegistrationModel(BaseModel):
    name: Optional[NAME] = None
    username: NAME
    email: EmailStr
    password: PASSWORD
    age: Optional[AGE] = None
    gender: Optional[Literal["M", "F", "O"]] = None
    role: USER_ROLES
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

        return value


class UpdateUser(BaseModel):
    name: Optional[NAME] = None
    username: Optional[NAME] = None
    email: Optional[EmailStr] = None
    password: Optional[PASSWORD] = None
    new_password: Optional[PASSWORD] = None
    age: Optional[AGE] = None
    role: Optional[USER_ROLES] = None
    gender: Optional[Literal["M", "F", "O"]] = None
    organization: Optional[ID] = None
    privacy_policy: Optional[bool] = None
    terms_and_conditions: Optional[bool] = None
    marketing_consent: Optional[bool] = None

    @field_validator("password")
    def validate_password(cls, value):
        if not value:
            return None
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")

        return value


class LoginModel(BaseModel):
    email_or_username: str
    password: str


class ResetPasswordModel(BaseModel):
    token: str
    new_password: PASSWORD

    @field_validator("new_password")
    def validate_password(cls, value):
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.islower() for c in value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")

        return value

    @field_validator("token", mode='before')
    def check_empty_token(cls, values):
        if not values or values == "":
            raise ValueError("Token field cannot be empty")
        return values
