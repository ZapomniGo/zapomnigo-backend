from flask import Blueprint, request

from src.controllers.utility_controller import UtilityController
from src.controllers.verification_controller import VerificationController as c
from src.database.repositories.users_repository import UsersRepository
from src.pydantic_models.mail_sender_model import MailSenderModel
from src.utilities.parsers import validate_json_body

verification_bp = Blueprint("verification", __name__)


@verification_bp.get("/verify")
def verify_user_route():
    verification_token = request.args["token"]
    return c.verify_user(verification_token)


@verification_bp.post("/send-email")
async def send_email():
    json_data = request.get_json()

    validation_errors = validate_json_body(json_data, MailSenderModel)  # type: ignore
    if validation_errors:
        return {"validation errors": validation_errors}, 422

    user_id = json_data["user_id"]
    username = json_data["username"]
    email = json_data["email"]

    if not UsersRepository.get_user_by_ulid(user_id):
        return {"message": "user doesn't exist"}, 404

    await UtilityController.send_mail_logic(email, user_id, username)
    return {"message": f"Email send to {email}"}, 200



