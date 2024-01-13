from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.config import DevConfig, ProdConfig, IS_OFFLINE, LocalConfig, IS_PROD, IS_DEV
from src.database.models.base import db
from src.routes import Routes
from src.utilities.exception_handlers import ExceptionHandlers

migrate = Migrate(directory="database/migrations")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/v1/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173",
                                                "https://dev-client-zapomnigo-192299046f7f.herokuapp.com",
                                                "https://prod-client-zapomnigo-3d223494b86d.herokuapp.com"]}}
         , supports_credentials=True)

    if IS_OFFLINE and not IS_PROD and not IS_DEV:
        app.config.from_object(LocalConfig)
    elif IS_PROD:
        app.config.from_object(ProdConfig)
    elif IS_DEV:
        app.config.from_object(DevConfig)

    Routes.register_blueprints(app)
    ExceptionHandlers.register_error_handlers(app)

    db.init_app(app)
    migrate.init_app(app, db)
    # Creates tables in the database based on the models if they don't exist
    with app.app_context():
        db.create_all()

    return app


asgi_app = WsgiToAsgi(create_app())


def start() -> None:
    create_app().run(host="0.0.0.0", port=3884)


if __name__ == '__main__':
    start()
