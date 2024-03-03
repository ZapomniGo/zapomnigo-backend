import ssl
import subprocess

from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from src.celery_task_queue.initializer import celery_init_app
from src.config import DevConfig, ProdConfig, IS_OFFLINE, LocalConfig, IS_PROD, IS_DEV
from src.database.models.base import db
from src.limiter import limiter
from src.routes import Routes
from src.utilities.exception_handlers import ExceptionHandlers

migrate = Migrate(directory="database/migrations")


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/api/v1/*": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173",
                                                    "https://dev-client-zapomnigo-192299046f7f.herokuapp.com",
                                                    "https://prod-client-zapomnigo-3d223494b86d.herokuapp.com",
                                                    "https://www.zapomnigo.com",
                                                    "https://zapomnigo.com",
                                                    "https://dev.zapomnigo.com",
                                                    "https://localhost"]}}
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
    limiter.init_app(app)
    celery_init_app(app)

    # Creates tables in the database based on the models if they don't exist
    with app.app_context():
        db.create_all()

    return app


def start() -> None:
    # This is when you do poetry run start
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile='data/certs/zapomnigo.crt', keyfile='data/certs/zapomnigo.key')
    # Start Celery worker and beat services
    subprocess.Popen(["celery", "-A", "src.celery_task_queue.make_celery", "worker", "--autoscale=8,1", "--loglevel", "INFO"])
    subprocess.Popen(["celery", "-A", "src.celery_task_queue.make_celery", "beat", "--loglevel", "INFO"])
    create_app().run(host="0.0.0.0", port=3884, ssl_context=ssl_context)


if __name__ == '__main__':
    start()
