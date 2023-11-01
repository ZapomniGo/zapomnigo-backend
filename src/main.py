from flask import Flask

from src.config import DevConfig, ProdConfig, IS_OFFLINE
from src.routes import Routes


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    if IS_OFFLINE:
        app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)

    Routes.register_blueprints(app)

    return app


def start() -> None:
    create_app().run(host="0.0.0.0")


if __name__ == '__main__':
    start()
