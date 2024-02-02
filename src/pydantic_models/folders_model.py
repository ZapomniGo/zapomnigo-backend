from typing import Optional, List

from pydantic import BaseModel, field_validator

from src.pydantic_models.common import ID
from src.pydantic_models.sets_model import SET_OR_FOLDER_NAME, SET_OR_FOLDER_DESCRIPTION


class FoldersModel(BaseModel):
    folder_title: SET_OR_FOLDER_NAME
    folder_description: Optional[SET_OR_FOLDER_DESCRIPTION] = None
    category_id: Optional[ID] = None
    subcategory_id: Optional[ID] = None
    sets: List[ID]
    organization_id: Optional[ID] = None

    @field_validator('sets', mode='before')
    def check_empty_sets(cls, values):
        if not values:
            raise ValueError("Sets list cannot be empty")
        return values

    @field_validator('folder_description', 'category_id', 'subcategory_id' 'organization_id', mode='before')
    def convert_empty_string_to_none(cls, value):
        return None if value == "" else value


class UpdateFoldersModel(BaseModel):
    # model_config = ConfigDict(extra='forbid')
    folder_title: Optional[SET_OR_FOLDER_NAME] = None
    folder_description: Optional[SET_OR_FOLDER_DESCRIPTION] = None
    category_id: Optional[ID] = None
    subcategory_id: Optional[ID] = None
    sets: List[ID]

    @field_validator('folder_description', 'category_id', 'subcategory_id', mode='before')
    def convert_empty_string_to_none(cls, value):
        return None if value == "" else value

    @field_validator('sets', mode='before')
    def check_empty_sets(cls, values):
        if not values:
            raise ValueError("Sets list cannot be empty")
        return values