from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.pydantic_models.common import NAME, ID


class CategoriesModel(BaseModel):
    category_name: NAME


class UpdateCategoriesModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    category_name: Optional[NAME] = None


class SubcategoriesModel(BaseModel):
    subcategory_name: NAME


class UpdateSubcategoriesModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

    subcategory_name: Optional[NAME] = None


class CategoriesWithSubcategoriesModel(BaseModel):
    subcategories: List[ID]