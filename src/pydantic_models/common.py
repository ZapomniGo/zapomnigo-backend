from typing import Annotated

from pydantic import StringConstraints

NAME = Annotated[str, StringConstraints(min_length=2, max_length=40)]