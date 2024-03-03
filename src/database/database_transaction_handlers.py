from functools import wraps

from src.database.models.base import db


# db.session is a session that is scoped to the current Flask application context.
# It is cleaned up after every request.


def handle_database_session_transaction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception:
            db.session.rollback()
            raise

    return wrapper
