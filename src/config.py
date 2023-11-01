from os import getenv


class DevConfig:
    SECRET_KEY = getenv("SECRET_KEY")
