from pydantic import BaseModel, EmailStr


class MailSenderModel(BaseModel):
    email: EmailStr
