from pydantic import BaseModel


class LoginModel(BaseModel):
    email_or_username: str
    password: str
