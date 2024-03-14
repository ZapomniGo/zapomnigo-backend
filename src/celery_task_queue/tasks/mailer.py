import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from celery import shared_task

from src.config import SENDER_EMAIL, SENDER_PASSWORD


def send_mail(receiver: str, subject: str, html: str) -> None:
    mime_msg = MIMEMultipart('alternative')

    mime_msg['From'] = SENDER_EMAIL
    mime_msg['Subject'] = subject
    mime_msg['To'] = receiver
    mime_msg.attach(MIMEText(html, "html"))

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver, mime_msg.as_string())

    server.close()


@shared_task(ignore_result=True)
def send_email_background_task(receiver: str, subject: str, html: str):
    send_mail(receiver, subject, html)
