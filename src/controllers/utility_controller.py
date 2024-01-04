import asyncio
from typing import Tuple, Dict, Any

from flask import request
from jwt import decode

from src.auth.jwt_creation import JwtCreation
from src.config import SECRET_KEY, ADMIN_USERNAME
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
        return decode(request.cookies.get('refresh_token'), SECRET_KEY, algorithms=["HS256"]).get("username")

    @classmethod
    async def send_mail_logic(cls, email: str, username: str, is_verification = True):
        token = JwtCreation.create_verification_jwt(username)
        if is_verification:
            BODY_HTML = f"""<html>
                    <head></head>
                    <body>
                      <h1>Hi welcome to our app, {username}</h1>
                      <p>Please verify your email by clicking
                        <a href='http://localhost:5173/verify?token={token}'>here</a></p>
                    </body>
                    </html>
                                """
        else:
            BODY_HTML = f"""<html>
                    <head></head>
                    <body>
                      <h1>Hello, {username}</h1>
                      <p>Please reset your password by clicking
                        <a href='http://127.0.0.1:8000/v1/forgot-password?token={token}'>here</a></p>
                    </body>
                    </html>
                                """

        asyncio.create_task(send_email_background_task(email, "TEST", BODY_HTML))
