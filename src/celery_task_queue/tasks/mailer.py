import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import getenv

from celery import shared_task


def send_mail(receiver: str, subject: str, html: str, attachment_path: str = None) -> None:
    port = 465  # SSL
    email = getenv("SENDER_EMAIL")
    password = getenv("SENDER_PASSWORD")

    mime_msg = MIMEMultipart('alternative')

    mime_msg['From'] = email
    mime_msg['Subject'] = subject
    mime_msg.attach(MIMEText(html, "html"))

    # attach file if provided
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=attachment_path)
        mime_msg.attach(part)

    server = smtplib.SMTP_SSL('smtp.gmail.com', port)
    server.login(email, password)
    server.sendmail(email, receiver, mime_msg.as_string())

    server.close()


@shared_task(ignore_result=True)
def send_email_background_task(receiver: str, subject: str, html: str, attachment_path: str = None):
    send_mail(receiver, subject, html, attachment_path)
