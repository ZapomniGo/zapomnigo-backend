from quart import Quart
from quart_cors import cors

from src.config import DevConfig, ProdConfig, IS_OFFLINE
from src.database.models.base import db
from src.routes import Routes
from src.utilities.exception_handlers import ExceptionHandlers

# migrate = Migrate(directory="database/migrations")
app = Quart(__name__, instance_relative_config=True)
app = cors(app, allow_origin=["http://127.0.0.1:3884", "https://zapomnigo-server-aaea6dc84a09.herokuapp.com/",
                              "http://0.0.0.0:3884", "http://127.0.0.1:5173", "http://0.0.0.1:5173"], allow_methods="*",
           allow_headers="*", allow_credentials=True)

if IS_OFFLINE:
    app.config.from_object(DevConfig)
else:
    app.config.from_object(ProdConfig)

Routes.register_blueprints(app)
ExceptionHandlers.register_error_handlers(app)

db.init_app(app)


# migrate.init_app(app, db)


def start() -> None:
    app.run(host="0.0.0.0", port=3884)


if __name__ == '__main__':
    start()
