from typing import List

from flask import Blueprint, Flask

from src.routes.categories_routes import categories_bp
from src.routes.flashcards_routes import flashcards_bp
from src.routes.folders_routes import folders_bp
from src.routes.organizations_routes import organizations_bp
from src.routes.sets_routes import sets_bp
from src.routes.subcategories_routes import subcategories_bp
from src.routes.subscription_models_routes import subscription_models_bp
from src.routes.users_routes import users_bp
from src.routes.utility_routes import utility_bp
from src.routes.verification_routes import verification_bp


class Routes:
    _blueprints: List[Blueprint] = [utility_bp, users_bp, subscription_models_bp, organizations_bp, categories_bp,
                                    subcategories_bp, sets_bp, flashcards_bp, verification_bp, folders_bp]

    @classmethod
    def register_blueprints(cls, app: Flask) -> None:
        for blueprint in cls._blueprints:
            app.register_blueprint(blueprint, url_prefix="/v1")
