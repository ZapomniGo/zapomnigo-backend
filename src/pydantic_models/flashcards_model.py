from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict, conint, field_validator

from src.pydantic_models.common import NAME, ID

TERM_DEFINITION = Annotated[str, StringConstraints(min_length=1, max_length=524288)]


class FlashcardsModel(BaseModel):
    term: TERM_DEFINITION
    definition: TERM_DEFINITION
    notes: Optional[TERM_DEFINITION] = None

    @field_validator('notes', mode='before')
    def convert_empty_string_to_none(cls, value):
        return None if value == "" else value


class UpdateFlashcardsModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    term: Optional[NAME] = None
    definition: Optional[TERM_DEFINITION] = None
    notes: Optional[TERM_DEFINITION] = None

    @field_validator('term', 'definition', 'notes', mode='before')
    def convert_empty_string_to_none(cls, value):
        return None if value == "" else value


class StudyFlashcardsModel(BaseModel):
    correctness: conint(ge=0, le=1)
    username: NAME
    user_id: ID
