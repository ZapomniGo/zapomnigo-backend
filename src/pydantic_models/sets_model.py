from typing import Optional, Annotated, List

from pydantic import BaseModel, StringConstraints, model_validator, field_validator

from src.pydantic_models.common import ID
from src.pydantic_models.flashcards_model import FlashcardsModel

SET_OR_FOLDER_DESCRIPTION = Annotated[str, StringConstraints(min_length=2, max_length=4096)]
SET_OR_FOLDER_NAME = Annotated[str, StringConstraints(min_length=1, max_length=255)]


class SetsModel(BaseModel):
    set_name: SET_OR_FOLDER_NAME
    set_description: Optional[SET_OR_FOLDER_DESCRIPTION] = None
    set_category: Optional[ID] = None
    set_subcategory: Optional[ID] = None
    flashcards: List[FlashcardsModel]
    organization_id: Optional[ID] = None

    @field_validator('set_description', 'set_category', 'set_subcategory', 'organization_id', mode='before')
    def convert_empty_string_to_none(cls, value):
        return None if value == "" else value

    @model_validator(mode='before')
    def check_empty_flashcards(cls, values):
        flashcards = values.get('flashcards')
        if not flashcards:
            raise ValueError("Flashcards list cannot be empty")
        return values


class UpdateSetsModel(BaseModel):
    # model_config = ConfigDict(extra='forbid')
    set_name: Optional[SET_OR_FOLDER_NAME] = None
    set_description: Optional[SET_OR_FOLDER_DESCRIPTION] = None
    set_category: Optional[ID] = None
    set_subcategory: Optional[ID] = None
    flashcards: Optional[List[FlashcardsModel]] = None

    @field_validator('set_name', 'set_description', 'set_category', 'set_subcategory', mode='before')
    def convert_empty_string_to_none(cls, value):
        return None if value == "" else value
