from pydantic import BaseModel, EmailStr


class MailSenderModel(BaseModel):
    email: EmailStr

class ReportSetModel(BaseModel):
    reason: str
