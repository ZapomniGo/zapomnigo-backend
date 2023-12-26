from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict

from src.pydantic_models.common import NAME

TERM_DEFINITION = Annotated[str, StringConstraints(min_length=1, max_length=16384)]


class FlashcardsModel(BaseModel):
    term: TERM_DEFINITION
    definition: TERM_DEFINITION
    notes: Optional[TERM_DEFINITION] = None
    set_id: str


class UpdateFlashcardsModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    term: Optional[NAME] = None
    definition: Optional[TERM_DEFINITION] = None
    notes: Optional[TERM_DEFINITION] = None
