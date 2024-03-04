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

if IS_OFFLINE:
    SECRET_KEY = getenv("DEV_SECRET_KEY")
    CELERY_BROKER_URL = getenv("LOCAL_CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = getenv("LOCAL_CELERY_RESULT_BACKEND")
    RATELIMIT_STORAGE_URI = getenv("LOCAL_RATELIMIT_STORAGE_URI")
else:
    # TODO: CHANGE PROD AND DEV SECRET KEYS
    SECRET_KEY = getenv("PROD_SECRET_KEY")
    CELERY_BROKER_URL = getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = getenv("CELERY_RESULT_BACKEND")
    RATELIMIT_STORAGE_URI = getenv("RATELIMIT_STORAGE_URI")


class DevConfig:
    SECRET_KEY = SECRET_KEY
    if not IS_OFFLINE:
        SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL").replace("postgres:", "postgresql+psycopg2:")
    else:
        SQLALCHEMY_DATABASE_URI = getenv("DEV_DATABASE_URL").replace("postgres:", "postgresql+psycopg2:")

    CELERY_BROKER_URL = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
    RATELIMIT_STORAGE_URI = RATELIMIT_STORAGE_URI


class LocalConfig:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = getenv("LOCAL_DATABASE_URI")
    DEBUG = True
    CELERY_BROKER_URL = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
    RATELIMIT_STORAGE_URI = RATELIMIT_STORAGE_URI


class ProdConfig:
    SECRET_KEY = SECRET_KEY
    if not IS_OFFLINE:
        SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL").replace("postgres:", "postgresql+psycopg2:")
    else:
        SQLALCHEMY_DATABASE_URI = getenv("PROD_DATABASE_URL").replace("postgres:", "postgresql+psycopg2:")

    CELERY_BROKER_URL = CELERY_BROKER_URL
    CELERY_RESULT_BACKEND = CELERY_RESULT_BACKEND
    RATELIMIT_STORAGE_URI = RATELIMIT_STORAGE_URI
