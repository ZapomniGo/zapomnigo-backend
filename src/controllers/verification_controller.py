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

        user = UsersRepository.get_user_by_ulid(response.get("user_id"))
        if not user:
            return {"message": "user doesn't exist"}, 404

        UsersRepository.change_verified_status(user)
        return {"Message": "Your account has been verified"}, 200

    @classmethod
    def verify_token(cls, token) -> Tuple[Dict[str, str], int]:
        if not token:
            return {"Message": "No verification token provided."}, 401
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return {"Message": "Verification link expired."}, 420
        except jwt.exceptions.InvalidSignatureError:
            return {"Message": "Invalid verification token signature."}, 401
        except jwt.exceptions.DecodeError:
            return {"Message": "Invalid or missing verification token."}, 499

        user_id = decoded_token.get("sub", None)
        if not user_id:
            return {"Message": "No user_id provided"}, 403

        return {"user_id": user_id}, 200
