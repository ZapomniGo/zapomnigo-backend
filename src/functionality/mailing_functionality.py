import asyncio

from src.config import IS_OFFLINE, IS_DEV, IS_PROD
from src.functionality.auth.auth_functionality import AuthFunctionality
from src.services.mailer import send_email_background_task


class EmailTemplates:
    templates = {
        "report": {
            "subject": "Докладване на сет/папка",
            "template_path": 'resources/email_templates/BG_Report.html'
        },
        "verification": {
            "subject": "Добре дошъл!",
            "template_path": 'resources/email_templates/BG_VerifyEmail.html'
        },
        "reset_password": {
            "subject": "Забравена парола",
            "template_path": 'resources/email_templates/BG_ResetPassword.html'
        },
        "change_email": {
            "subject": "Промяна на имейл",
            "template_path": 'resources/email_templates/BG_ChangeEmail.html'
        },
        "change_password": {
            "subject": "Промяна на парола",
            "template_path": 'resources/email_templates/BG_ChangePassword.html'
        }
    }

    @classmethod
    def get_template(cls, template_name):
        return cls.templates.get(template_name)


class MailingFunctionality:
    @classmethod
    def get_base_url(cls):
        if IS_OFFLINE:
            return "http://localhost:5173"
        if IS_DEV:
            return "https://dev-client-zapomnigo-192299046f7f.herokuapp.com"
        elif IS_PROD:
            return "https://zapomnigo.com"

    @classmethod
    async def send_mail_logic(cls, email: str, username: str, template_name: str, report_body=None):
        token = AuthFunctionality.create_jwt_token(username, is_refresh=False)
        template = EmailTemplates.get_template(template_name)

        if template_name == "report":
            body_html = report_body
        else:
            body_html = cls.generate_email_body(username, token, template["template_path"])

        asyncio.create_task(send_email_background_task(email, template["subject"], body_html))

    @classmethod
    def generate_email_body(cls, username, token, template_path):
        base_url = cls.get_base_url()
        url = f'{base_url}/app/{template_path.split("/")[-1].split(".")[0]}?token={token}'

        html_content = cls.read_html_template(template_path)
        html_content = html_content.replace("{username}", username)
        html_content = html_content.replace("{url}", url)
        html_content = html_content.replace("{base_url}", base_url)

        return html_content

    @classmethod
    async def send_change_email_logic(cls, email: str, username: str):
        token = AuthFunctionality.create_jwt_token(username, is_refresh=False)
        template = EmailTemplates.get_template("change_email")

        body_html = cls.generate_email_body(username, token, template["template_path"])

        asyncio.create_task(send_email_background_task(email, template["subject"], body_html))

    @classmethod
    async def send_change_password_logic(cls, email: str, username: str):
        token = AuthFunctionality.create_jwt_token(username, is_refresh=False)
        template = EmailTemplates.get_template("change_password")

        body_html = cls.generate_email_body(username, token, template["template_path"])

        asyncio.create_task(send_email_background_task(email, template["subject"], body_html))

    @classmethod
    def read_html_template(cls, template_path):
        with open(template_path, 'r') as file:
            return file.read()
