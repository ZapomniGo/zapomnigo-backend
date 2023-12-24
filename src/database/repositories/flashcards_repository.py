from typing import List

from src.database.models import Flashcards
from src.database.models.base import db


class FlashcardsRepository:
    @classmethod
    def get_flashcard_by_id(cls, flashcard_id: str) -> Flashcards | None:
        return db.session.query(Flashcards).filter_by(flashcard_id=flashcard_id).first()

    @classmethod
    def get_flashcards_by_set_id(cls, set_id: str) -> List[Flashcards]:
        return db.session.query(Flashcards).filter_by(set_id=set_id).all()

    # @classmethod
    # def edit_set(cls, set_obj: Flashcards, json_data: Dict[str, Any]) -> None:
    #     set_obj.set_name = json_data.get("set_name", set_obj.set_name)
    #     set_obj.set_description = json_data.get("set_description", set_obj.set_description)
    #     set_obj.set_modification_date = str(datetime.now())
    #
    #     try:
    #         # Checks for falsify values like "" and None
    #         if not json_data["set_category"]:
    #             set_obj.set_category = None
    #         else:
    #             set_obj.set_category = json_data["set_category"]
    #     except KeyError:
    #         set_obj.set_category = set_obj.set_category
    #
    #     db.session.commit()
