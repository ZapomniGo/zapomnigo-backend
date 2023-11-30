from pydantic import BaseModel

from src.pydantic_models.common import NAME


class CategoriesModel(BaseModel):
    category_name: NAME
