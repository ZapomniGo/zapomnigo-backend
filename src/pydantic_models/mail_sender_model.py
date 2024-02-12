from pydantic import BaseModel, EmailStr


class MailSenderModel(BaseModel):
    email: EmailStr

class ReportFolderSetModel(BaseModel):
    reason: str
