from typing import List

from flask import Blueprint, Flask

from src.routes.organizations_routes import organizations_bp
from src.routes.subscription_models_routes import subscription_models_bp
from src.routes.users_routes import users_bp
from src.routes.utility_routes import utility_bp


class Routes:
    _blueprints: List[Blueprint] = [utility_bp, users_bp, subscription_models_bp, organizations_bp]

    @classmethod
    def register_blueprints(cls, app: Flask) -> None:
        for blueprint in cls._blueprints:
            app.register_blueprint(blueprint, url_prefix="/v1")
