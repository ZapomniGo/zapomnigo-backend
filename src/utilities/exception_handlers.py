from traceback import format_exc

from flask import request, Flask

from src.config import IS_OFFLINE


class ExceptionHandlers:
    @classmethod
    def handle_uncaught_exception(cls, exc: Exception):
        content = {"message": "Something went wrong, please contact ZapomniGo!"}

        if IS_OFFLINE:
            content = {"message": "I am going to cut your legs off",
                       "exception": str(exc),
                       "http_method": request.method,
                       "url": str(request.url),
                       "body": None if request.data == b'' else str(request.get_json()),
                       "stacktrace": format_exc()}

        return content, 500

    @classmethod
    def register_error_handlers(cls, app: Flask):
        app.register_error_handler(Exception, cls.handle_uncaught_exception)
