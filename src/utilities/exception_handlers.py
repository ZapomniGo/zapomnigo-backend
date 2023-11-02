from flask import Request, request

from src.config import IS_OFFLINE
from traceback import format_exc


# The request Content-Type should be 'application/json'
class ExceptionHandlers:
    @staticmethod
    def handle_uncaught_exception(exc: Exception):
        content = {"message": "Something went wrong, please contact ZapomniGo!"}

        if IS_OFFLINE:
            content = {"exception": str(exc),
                       "http_method": request.method,
                       "url": str(request.url),
                       "body": None if request.data == b'' else str(request.get_json()),
                       "stacktrace": format_exc()}

        return content, 500
