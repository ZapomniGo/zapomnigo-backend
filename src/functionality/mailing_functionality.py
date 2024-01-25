import asyncio

from src.config import IS_OFFLINE, IS_DEV, IS_PROD
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.services.mailer import send_email_background_task


class MailingFunctionality:
    @classmethod
    async def send_mail_logic(cls, email: str, username: str, is_verification=True):
        token = AuthFunctionality.create_jwt_token(username, is_refresh=False)
        if is_verification:
            body_html = cls.generate_email_body(username, token, True)
            subject = "Добре дошъл!"
        else:
            body_html = cls.generate_email_body(username, token, False)
            subject = "Забравена парола"

        asyncio.create_task(send_email_background_task(email, subject, body_html))

    @classmethod
    def generate_email_body(cls, username, token, is_verification):
        base_url = ""
        if IS_OFFLINE:
            base_url = "http://localhost:5173"
        if IS_DEV:
            base_url = "https://dev-client-zapomnigo-192299046f7f.herokuapp.com"
        elif IS_PROD:
            base_url = "https://zapomnigo.com"

        if is_verification:
            template_path = 'resources/email_templates/BG_VerifyEmail.html'
            url = f'{base_url}/app/verify?token={token}'
        else:
            template_path = 'resources/email_templates/BG_ResetPassword.html'
            url = f'{base_url}/app/forgot-password?token={token}'

        html_content = cls.read_html_template(template_path)
        html_content = html_content.replace("{username}", username)
        html_content = html_content.replace("{url}", url)
        html_content = html_content.replace("{base_url}", base_url)

        return html_content

    @classmethod
    def read_html_template(cls, template_path):
        with open(template_path, 'r') as file:
            return file.read()
