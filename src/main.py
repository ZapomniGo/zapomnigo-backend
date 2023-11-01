from flask import Flask

from src.config import DevConfig
from src.routes import Routes


def create_app(config_class=DevConfig) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    Routes.register_blueprints(app)

    return app


def start() -> None:
    create_app().run(host="0.0.0.0", debug=True, load_dotenv=True)


if __name__ == '__main__':
    start()
