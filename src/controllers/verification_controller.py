from typing import Tuple, Dict

import jwt

from src.config import SECRET_KEY
from src.controllers.users_controller import UsersController
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
    def verify_token(cls, token) -> Tuple[Dict[str, str], int]:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"message": "Verification link expired."}, 420
        except jwt.exceptions.InvalidSignatureError:
            return {"message": "Invalid verification token signature."}, 401
        except jwt.exceptions.DecodeError:
            return {"message": "Invalid or missing verification token."}, 499

        username = decoded_token.get("sub", None)
        if not username:
            return {"message": "No user_id provided"}, 499

        return {"username": username}, 200
