import asyncio
from typing import Tuple, Dict, Any

from flask import request
from jwt import decode

from src.auth.jwt_creation import JwtCreation
from src.config import SECRET_KEY, ADMIN_USERNAME, IS_OFFLINE, IS_PROD, IS_DEV
from src.services.mailer import send_email_background_task


class UtilityController:

    @staticmethod
    def get_health() -> Tuple[Dict[str, str], int]:
        return {"status": "healthy"}, 200

    @classmethod
    def check_user_access(cls, username: str) -> Tuple[Dict[str, Any], int] | None:
        """Returns a JSON Response if there is an error or the user doesn't have access"""
        logged_in_username = cls.get_session_username()
        if not logged_in_username:
            return {"message": "No username provided"}, 400

        if logged_in_username == ADMIN_USERNAME or logged_in_username == username:
            return None

        return {"message": "Admin privileges required."}, 403

    @classmethod
    def get_session_username(cls) -> str | None:
        access_token = request.headers.get('Authorization')
        if access_token:
            return decode(access_token, SECRET_KEY, algorithms=["HS256"]).get("username")
        else:
            return None

    @classmethod
    async def send_mail_logic(cls, email: str, username: str, is_verification=True):
        token = JwtCreation.create_verification_jwt(username)
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
            base_url = "https://prod-client-zapomnigo-3d223494b86d.herokuapp.com"

        if is_verification:
            template_path = '../resources/email_templates/BG_VerifyEmail.html'
            url = f'{base_url}/verify?token={token}'
        else:
            template_path = '../resources/email_templates/BG_ResetPassword.html'
            url = f'{base_url}/forgot-password?token={token}'

        html_content = cls.read_html_template(template_path)
        html_content = html_content.replace("{username}", username)
        html_content = html_content.replace("{url}", url)
        html_content = html_content.replace("{base_url}", base_url)

        return html_content

    @classmethod
    def read_html_template(cls, template_path):
        with open(template_path, 'r') as file:
            return file.read()
