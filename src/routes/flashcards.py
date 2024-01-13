from typing import Tuple, Dict, Any

from flask import Blueprint

from src.auth.jwt_decorators import jwt_required
from src.controllers.flashcards_contoller import FlashcardsController as c

flashcards_bp = Blueprint("flashcards", __name__)


@flashcards_bp.get("/flashcards/<flashcard_id>")
def get_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_flashcard(flashcard_id)


@flashcards_bp.delete("/flashcards/<flashcard_id>")
@jwt_required
def delete_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_flashcard(flashcard_id)


@flashcards_bp.put("/flashcards/<flashcard_id>")
@jwt_required
def update_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    return c.update_flashcard(flashcard_id)
@flashcards_bp.put("/flashcards/<flashcard_id>/study")
@jwt_required
def study_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    return c.study_flashcard(flashcard_id)