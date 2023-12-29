from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv

from aiosmtplib import SMTP


async def send_mail(receiver: str, subject: str, html: str) -> None:
    port = 465  # SSL
    email = getenv("SENDER_EMAIL")
    password = getenv("SENDER_PASSWORD")

    mime_msg = MIMEMultipart('alternative')

    mime_msg['From'] = email
    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    async with SMTP(hostname='smtp.gmail.com', port=port, use_tls=True) as server:
        await server.login(email, password)
        await server.sendmail(email, receiver, mime_msg.as_string())


async def send_email_background_task(receiver: str, subject: str, html: str):
    await send_mail(receiver, subject, html)
