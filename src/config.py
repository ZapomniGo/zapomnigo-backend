from os import getenv

from dotenv import load_dotenv

from src.utilities.parsers import eval_bool

load_dotenv()

IS_OFFLINE = eval_bool(getenv("IS_OFFLINE", False))


class DevConfig:
    SECRET_KEY = getenv("DEV_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DEV_DATABASE_URI")
    DEBUG = True


class ProdConfig:
    SECRET_KEY = getenv("PROD_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URL")
