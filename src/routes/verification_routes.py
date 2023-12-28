from flask import Blueprint, request

from src.controllers.verification_controller import VerificationController as c

verification_bp = Blueprint("verification", __name__)


@verification_bp.get("/verify")
def verify_user_route():
    verification_token = request.args["token"]
    return c.verify_user(verification_token)
