from typing import Tuple, Dict

import jwt

from src.config import SECRET_KEY
from src.database.repositories.users_repository import UsersRepository


class VerificationController:

    @classmethod
    def verify_user(cls, token) -> Tuple[Dict[str, str], int]:
        response, status_code = cls.verify_token(token)
        if status_code != 200:
            return response, status_code

        user = UsersRepository.get_user_by_username(response.get("username"))
        if not user:
            return {"message": "user doesn't exist"}, 404

        UsersRepository.change_verified_status(user)
        return {"message": "Your account has been verified"}, 200

    @classmethod
    def decode_query_param_token(cls, token, is_verification=True):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            message = "Verification link expired." if is_verification else "Reset password link expired."
            return {"message": message}, 420
        except jwt.exceptions.InvalidSignatureError:
            message = "Invalid verification token signature." if is_verification else "Invalid reset password token signature."
            return {"message": message}, 401
        except jwt.exceptions.DecodeError:
            message = "Invalid verification link." if is_verification else "Invalid reset password link."
            return {"message": message}, 499

        return decoded_token, 200

    @classmethod
    def verify_token(cls, token, is_verification=True) -> Tuple[Dict[str, str], int]:
        """This method is used to verify the validity and integrity of the jwt_token used in the urls for verifying
        emails and changing passwords."""

        response, status_code = cls.decode_query_param_token(token, is_verification)
        if status_code != 200:
            return response, status_code

        username = response.get("username", None)
        if not username:
            return {"message": "No username provided"}, 499

        return {"username": username}, 200
