from typing import Optional, List

from pydantic import BaseModel, model_validator

from src.pydantic_models.sets_model import ID, SET_OR_FOLDER_NAME, SET_OR_FOLDER_DESCRIPTION, SetsModel


class FoldersModel(BaseModel):
    folder_title: SET_OR_FOLDER_NAME
    folder_description: Optional[SET_OR_FOLDER_DESCRIPTION] = None
    category_id: Optional[ID] = None
    sets: List[SetsModel]
    organization_id: Optional[ID] = None

    @model_validator(mode='before')
    def check_empty_sets(cls, values):
        sets = values.get('sets')
        if not sets:
            raise ValueError("Sets list cannot be empty")
        return values


class UpdateFoldersModel(BaseModel):
    # model_config = ConfigDict(extra='forbid')
    folder_title: Optional[SET_OR_FOLDER_NAME] = None
    folder_description: Optional[SET_OR_FOLDER_DESCRIPTION] = None
    category_id: Optional[ID] = None
    sets: Optional[List[SetsModel]] = None
