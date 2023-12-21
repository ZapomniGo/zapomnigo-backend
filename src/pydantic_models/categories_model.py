from typing import Optional

from pydantic import BaseModel, ConfigDict

from src.pydantic_models.common import NAME


class CategoriesModel(BaseModel):
    category_name: NAME


class UpdateCategoriesModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    category_name: Optional[NAME] = None
