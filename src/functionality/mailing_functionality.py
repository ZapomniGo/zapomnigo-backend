from enum import Enum

from src.celery_task_queue.tasks.mailer import send_email_background_task
from src.config import IS_OFFLINE, IS_DEV, IS_PROD
from src.functionality.auth.auth_functionality import AuthFunctionality


class TemplateNames(Enum):
    VERIFICATION = "verification"
    RESET_PASSWORD = "reset_password"
    CHANGE_EMAIL = "change_email"
    CHANGE_PASSWORD = "change_password"
    DELETE_USER = "delete-user"


class MailingFunctionality:
    TEMPLATES = {
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
            "template_path": 'resources/email_templates/BG_ChangedEmail.html'
        },
        "change_password": {
            "subject": "Промяна на парола",
            "template_path": 'resources/email_templates/BG_ChangedPassword.html'
        },
        "delete-user": {
            "subject": "Изтриване на акаунт",
            "template_path": 'resources/email_templates/BG_DeletedAccount.html'
        }
    }

    @classmethod
    def get_template(cls, template_name):
        return cls.TEMPLATES.get(template_name)

    @classmethod
    def get_base_url(cls):
        if IS_OFFLINE:
            return "http://localhost:5173"
        if IS_DEV:
            return "https://dev-client-zapomnigo-192299046f7f.herokuapp.com"
        elif IS_PROD:
            return "https://zapomnigo.com"

    @classmethod
    def generate_email_body(cls, template_path, username: str | None = None, token: str | None = None,
                            is_verification_email: bool = True):
        """If is_verification_email is true, the url in the email is for verifying the email.
        If is_verification_email is false, the url in the email is for resetting the password."""

        base_url = cls.get_base_url()

        if is_verification_email:
            url = f"{base_url}/app/verify?token={token}"
        else:
            url = f"{base_url}/app/forgot-password?token={token}"

        html_content = cls.read_html_template(template_path)
        html_content = html_content.replace("{username}", username)
        html_content = html_content.replace("{url}", url)
        html_content = html_content.replace("{base_url}", base_url)

        return html_content

    # The asyncio.create_task is not awaited because the func is awaited in the controller
    @classmethod
    def send_report_email(cls, email: str, report_body: str):
        send_email_background_task.apply_async(args=[email, "Докладване на сет/папка", report_body], expires=1800)

    @classmethod
    def send_verification_email(cls, email: str, username: str, verify_on_register: bool = True):
        """If verify_on_register is true, the email will be sent when the user registers or requests a
        new verification email.
        If verify_on_register is false, the email will be sent when the user changes their email."""

        token = AuthFunctionality.create_jwt_token(username, is_refresh=False)

        if verify_on_register:
            template = cls.get_template(TemplateNames.VERIFICATION.value)
        else:
            template = cls.get_template(TemplateNames.CHANGE_EMAIL.value)

        body_html = cls.generate_email_body(template["template_path"], username, token)

        send_email_background_task.apply_async(args=[email, template["subject"], body_html], expires=1800)

    @classmethod
    def send_reset_password_email(cls, email: str, username: str, is_change_password: bool = False):
        token = AuthFunctionality.create_jwt_token(username, is_refresh=False)

        if not is_change_password:
            template = cls.get_template(TemplateNames.RESET_PASSWORD.value)
        else:
            template = cls.get_template(TemplateNames.CHANGE_PASSWORD.value)

        body_html = cls.generate_email_body(template["template_path"], username, token, is_verification_email=False)

        send_email_background_task.apply_async(args=[email, template["subject"], body_html], expires=1800)

    @classmethod
    def send_delete_user_email(cls, email: str, username: str):
        template = cls.get_template(TemplateNames.DELETE_USER.value)
        body_html = cls.generate_email_body(template["template_path"], username)

        send_email_background_task.apply_async(args=[email, template["subject"], body_html], expires=1800)

    @classmethod
    def read_html_template(cls, template_path):
        with open(template_path, 'r') as file:
            return file.read()
