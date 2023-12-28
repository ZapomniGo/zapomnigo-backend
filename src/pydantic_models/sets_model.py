from typing import Optional, Annotated, List

from pydantic import BaseModel, StringConstraints, ConfigDict, model_validator

from src.pydantic_models.flashcards_model import FlashcardsModel

SET_DESCRIPTION = Annotated[str, StringConstraints(min_length=2, max_length=4096)]
SET_NAME = Annotated[str, StringConstraints(min_length=1, max_length=255)]
ORGANIZATION_ID = Annotated[str, StringConstraints(max_length=26)]


class SetsModel(BaseModel):
    set_name: SET_NAME
    set_description: Optional[SET_DESCRIPTION] = None
    set_category: Optional[ORGANIZATION_ID] = None
    flashcards: List[FlashcardsModel]
    organization_id: Optional[ORGANIZATION_ID] = None

    @model_validator(mode='before')
    def check_empty_flashcards(cls, values):
        flashcards = values.get('flashcards')
        if not flashcards:
            raise ValueError("Flashcards list cannot be empty")
        return values


class UpdateSetsModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    set_name: Optional[SET_NAME] = None
    set_description: Optional[SET_DESCRIPTION] = None
    set_category: Optional[ORGANIZATION_ID] = None
    flashcards: List[FlashcardsModel] = None
