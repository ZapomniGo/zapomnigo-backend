from typing import List

from flask import Blueprint, Flask

from src.routes.utility_routes import utility_bp


class Routes:
    _blueprints: List[Blueprint] = [utility_bp]

    @classmethod
    def register_blueprints(cls, app: Flask) -> None:
        for blueprint in cls._blueprints:
            app.register_blueprint(blueprint, url_prefix="/v1")
