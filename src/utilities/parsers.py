from typing import Dict, Any, List

from pydantic import ValidationError, BaseModel


def eval_bool(bl: str | bool) -> bool:
    if type(bl) == bool:
        return bl
    else:
        bl = bl.strip().lower()
        if bl == "true":
            return True
        else:
            return False


def validate_json_body(json_data: Dict[str, Any], pydantic_model: BaseModel) -> List[Dict[str, Any]] | None:
    try:
        pydantic_model.model_validate(json_data, strict=True)
        return None
    except ValidationError as e:
        errors = []
        for error in e.errors():
            error_dict = {
                str(*error['loc']): error["msg"]
            }
            errors.append(error_dict)

        return errors
