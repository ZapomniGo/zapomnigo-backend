from traceback import format_exc

from quart import request, Quart
from jwt import ExpiredSignatureError, InvalidSignatureError, DecodeError
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException

from src.config import IS_OFFLINE
from src.database.models.base import db


class ExceptionHandlers:
    @classmethod
    def handle_uncaught_exception(cls, exc: Exception):

        if isinstance(exc, HTTPException):
            return exc

        content = {"message": "I am going to cut your legs off",
                   "exception": str(exc),
                   "http_method": request.method,
                   "url": str(request.url),
                   "body": None if request.data == b'' else str(request.get_json()),
                   "stacktrace": format_exc()}
        db.session.rollback()
        return content, 500

    @classmethod
    def handle_sqlalchemy_integrity_error(cls, exc: IntegrityError):
        db.session.rollback()
        error = str(exc)
        start_index = error.find("DETAIL:") + len("DETAIL:")
        end_index = error.find("[")
        error_message = error[start_index:end_index].strip()
        return {"error": error_message}, 409

    @classmethod
    def handle_token_expired_exception(cls, exc: ExpiredSignatureError):
        return {"message": "Auth token expired."}, 498

    @classmethod
    def handle_invalid_signature(cls, exd: InvalidSignatureError):
        return {"message": "Invalid token signature."}, 401

    @classmethod
    def handle_decode_error(cls, exc: DecodeError):
        return {"message": "Invalid or missing auth token."}, 499

    @classmethod
    def register_error_handlers(cls, app: Quart):
        if IS_OFFLINE:
            app.register_error_handler(Exception, cls.handle_uncaught_exception)

        app.register_error_handler(IntegrityError, cls.handle_sqlalchemy_integrity_error)
        app.register_error_handler(ExpiredSignatureError, cls.handle_token_expired_exception)
        app.register_error_handler(InvalidSignatureError, cls.handle_invalid_signature)
        app.register_error_handler(DecodeError, cls.handle_decode_error)
