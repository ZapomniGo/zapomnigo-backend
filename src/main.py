from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.config import DevConfig, ProdConfig, IS_OFFLINE
from src.database.models.base import db
from src.routes import Routes
from src.utilities.exception_handlers import ExceptionHandlers

migrate = Migrate(directory="database/migrations")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/v1/*": {"origins": "*"}}, supports_credentials=True)

    if IS_OFFLINE:
        app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)

    Routes.register_blueprints(app)
    ExceptionHandlers.register_error_handlers(app)

    db.init_app(app)
    migrate.init_app(app, db)
    # Creates tables in the database based on the models if they don't exist
    with app.app_context():
        db.create_all()

    return app


def start() -> None:
    create_app().run(host="0.0.0.0", port=3884)


if __name__ == '__main__':
    start()
