from dotenv import load_dotenv
from os import getenv

load_dotenv()


class DevConfig:
    SECRET_KEY = getenv("SECRET_KEY")
