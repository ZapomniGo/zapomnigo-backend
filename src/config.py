from os import getenv

from dotenv import load_dotenv

from src.utilities.parsers import eval_bool

load_dotenv()

IS_OFFLINE = eval_bool(getenv("IS_OFFLINE", True))
IS_PROD = eval_bool(getenv("IS_PROD", False))
IS_DEV = eval_bool(getenv("IS_DEV", False))

ADMIN_EMAIL = getenv("ADMIN_EMAIL")
ADMIN_USERNAME = getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

SENDER_EMAIL = getenv("SENDER_EMAIL")
SENDER_PASSWORD = getenv("SENDER_PASSWORD")

API_URL = getenv("API_URL")

if IS_OFFLINE:
    SECRET_KEY = getenv("DEV_SECRET_KEY")
else:
    # TODO: CHANGE PROD AND DEV SECRET KEYS
    SECRET_KEY = getenv("PROD_SECRET_KEY")


# This is done so that I can connect to the dev or prod db using poetry run start and having the
# other services running locally IS_OFFLINE=True is a requirement for this to work.
class DevConfig:
    SECRET_KEY = SECRET_KEY
    if not IS_OFFLINE:
        SQLALCHEMY_DATABASE_URI = getenv("DEV_DATABASE_URL")
        CELERY_BROKER_URL = getenv("PROD_CELERY_BROKER_URL")
        CELERY_RESULT_BACKEND = getenv("PROD_CELERY_RESULT_BACKEND")
        RATELIMIT_STORAGE_URI = getenv("PROD_RATELIMIT_STORAGE_URI")
    else:
        SQLALCHEMY_DATABASE_URI = getenv("DEV_DATABASE_URL")
        CELERY_BROKER_URL = getenv("LOCAL_CELERY_BROKER_URL")
        CELERY_RESULT_BACKEND = getenv("LOCAL_CELERY_RESULT_BACKEND")
        RATELIMIT_STORAGE_URI = getenv("LOCAL_RATELIMIT_STORAGE_URI")


class LocalConfig:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = getenv("LOCAL_DATABASE_URI")
    DEBUG = True
    CELERY_BROKER_URL = getenv("LOCAL_CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = getenv("LOCAL_CELERY_RESULT_BACKEND")
    RATELIMIT_STORAGE_URI = getenv("LOCAL_RATELIMIT_STORAGE_URI")


class ProdConfig:
    SECRET_KEY = SECRET_KEY
    if not IS_OFFLINE:
        SQLALCHEMY_DATABASE_URI = getenv("PROD_DATABASE_URL")
        CELERY_BROKER_URL = getenv("PROD_CELERY_BROKER_URL")
        CELERY_RESULT_BACKEND = getenv("PROD_CELERY_RESULT_BACKEND")
        RATELIMIT_STORAGE_URI = getenv("PROD_RATELIMIT_STORAGE_URI")
    else:
        SQLALCHEMY_DATABASE_URI = getenv("PROD_DATABASE_URL")
        CELERY_BROKER_URL = getenv("LOCAL_CELERY_BROKER_URL")
        CELERY_RESULT_BACKEND = getenv("LOCAL_CELERY_RESULT_BACKEND")
        RATELIMIT_STORAGE_URI = getenv("LOCAL_RATELIMIT_STORAGE_URI")
