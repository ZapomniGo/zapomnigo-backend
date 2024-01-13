from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict, Field, conint

from src.pydantic_models.common import NAME

TERM_DEFINITION = Annotated[str, StringConstraints(min_length=1, max_length=524288)]


class FlashcardsModel(BaseModel):
    term: TERM_DEFINITION
    definition: TERM_DEFINITION
    notes: Optional[TERM_DEFINITION] = None


class UpdateFlashcardsModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    term: Optional[NAME] = None
    definition: Optional[TERM_DEFINITION] = None
    notes: Optional[TERM_DEFINITION] = None


class StudyFlashcardsModel(BaseModel):
    correctness: conint(ge=0, le=1)
    username: NAME
    user_id: Annotated[str, StringConstraints(max_length=26)]
