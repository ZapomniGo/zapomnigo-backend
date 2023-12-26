from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict

from src.pydantic_models.common import NAME

DEFINITION = Annotated[str, StringConstraints(min_length=2, max_length=255)]


class FlashcardsModel(BaseModel):
    term: NAME
    definition: DEFINITION
    notes: Optional[DEFINITION] = None
    set_id: str


class UpdateFlashcardsModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    term: Optional[NAME] = None
    definition: Optional[DEFINITION] = None
    notes: Optional[DEFINITION] = None
