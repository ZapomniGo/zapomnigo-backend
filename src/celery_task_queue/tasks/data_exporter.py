from typing import Tuple, Dict, Any

from celery import shared_task

from src.database.repositories.users_repository import UsersRepository
from src.functionality.users_functionallity import UsersFunctionality


@shared_task(ignore_result=False)
def export_user_data_task(user_id: str) -> Tuple[Dict[str, Any], int]:
    user = UsersRepository.get_user_by_ulid(user_id)

    return {"user_info": UsersFunctionality.export_user_data(user)}, 200
