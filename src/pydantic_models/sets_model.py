from typing import Optional, Annotated

from pydantic import BaseModel, StringConstraints

from src.pydantic_models.common import NAME

SET_DESCRIPTION = Annotated[str, StringConstraints(min_length=2, max_length=255)]


class SetsModel(BaseModel):
    set_name: NAME
    set_description: Optional[SET_DESCRIPTION] = None
    set_category: str
