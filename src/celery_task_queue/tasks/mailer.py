import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv

from celery import shared_task


def send_mail(receiver: str, subject: str, html: str) -> None:
    port = 465  # SSL
    email = getenv("SENDER_EMAIL")
    password = getenv("SENDER_PASSWORD")

    mime_msg = MIMEMultipart('alternative')

    mime_msg['From'] = email
    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    server = smtplib.SMTP_SSL('smtp.gmail.com', port)
    server.login(email, password)
    server.sendmail(email, receiver, mime_msg.as_string())

    server.close()


@shared_task(ignore_result=True)
def send_email_background_task(receiver: str, subject: str, html: str):
    send_mail(receiver, subject, html)
