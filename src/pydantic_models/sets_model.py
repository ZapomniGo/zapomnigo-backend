from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints, ConfigDict

from src.pydantic_models.common import NAME

SET_DESCRIPTION = Annotated[str, StringConstraints(min_length=2, max_length=4096)]
SET_NAME = Annotated[str, StringConstraints(min_length=1, max_length=255)]


class SetsModel(BaseModel):
    set_name: SET_NAME
    set_description: Optional[SET_DESCRIPTION] = None
    set_category: str


class UpdateSetsModel(BaseModel):
    model_config = ConfigDict(extra='forbid')
    set_name: Optional[SET_NAME] = None
    set_description: Optional[SET_DESCRIPTION] = None
    set_category: Optional[str] = None
