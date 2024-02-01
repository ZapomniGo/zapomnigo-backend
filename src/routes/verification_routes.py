from flask import Blueprint, request
from flask_limiter.util import get_remote_address

from src.controllers.verification_controller import VerificationController as c
from src.database.repositories.users_repository import UsersRepository
from src.functionality.mailing_functionality import MailingFunctionality
from src.limiter import limiter
from src.pydantic_models.mail_sender_model import MailSenderModel
from src.utilities.parsers import validate_json_body, eval_bool

verification_bp = Blueprint("verification", __name__)


@verification_bp.get("/verify")
def verify_user_route():
    verification_token = request.args.get("token")
    if not verification_token:
        return {"Invalid verification link"}, 400
    return c.verify_user(verification_token)


@verification_bp.post("/send-email")
# @limiter.limit("5/hour")
async def send_email():
    is_verification = request.args.get("verification")
    if not is_verification:
        return {"message": "invalid argument provided"}, 404
    if is_verification.lower() == "true" or is_verification.lower() == "false":
        is_verification = eval_bool(is_verification)
    else:
        return {"message": "invalid argument provided"}, 404

    json_data = request.get_json()
    validation_errors = validate_json_body(json_data, MailSenderModel)
    if validation_errors:
        return {"validation errors": validation_errors}, 422

    email = json_data["email"]
    user = UsersRepository.get_user_by_email(email)
    if not user:
        return {"message": "user doesn't exist"}, 404

    await MailingFunctionality.send_mail_logic(user.email, user.username,is_verification=is_verification)
    return {"message": f"Email send to {email}"}, 200
