from typing import Annotated

from pydantic import StringConstraints, BaseModel

NAME = Annotated[str, StringConstraints(min_length=2, max_length=40)]
ID = Annotated[str, StringConstraints(max_length=26)]
PASSWORD = Annotated[str, StringConstraints(min_length=8, max_length=80)]


class VerifySetFolderModel(BaseModel):
    verified: bool
