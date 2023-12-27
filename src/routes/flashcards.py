from typing import Tuple, Dict, Any

from quart import Blueprint, request

from src.auth.jwt_decorators import jwt_required
from src.controllers.flashcards_contoller import FlashcardsController as c

flashcards_bp = Blueprint("flashcards", __name__)


@flashcards_bp.get("/flashcards/<flashcard_id>")
async def get_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    return c.get_flashcard(flashcard_id)


@flashcards_bp.delete("/flashcards/<flashcard_id>")
@jwt_required
async def delete_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    return c.delete_flashcard(flashcard_id)


@flashcards_bp.put("/flashcards/<flashcard_id>")
@jwt_required
async def update_flashcard(flashcard_id: str) -> Tuple[Dict[str, Any], int]:
    json_data = await request.get_json()
    return c.update_flashcard(flashcard_id, json_data)
