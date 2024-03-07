import logging
from typing import Dict, Any

from celery import shared_task
from celery.result import AsyncResult
from celery.signals import task_success, task_failure, task_postrun

from src.database.repositories.users_repository import UsersRepository
from src.functionality.users_functionallity import UsersFunctionality


@shared_task(ignore_result=False)
def export_user_data_task(user_id: str) -> Dict[str, Any]:
    user = UsersRepository.get_user_by_ulid(user_id)
    # raise Exception("This is a test exception")
    return {"user_data": UsersFunctionality.export_user_data(user)}


@task_success.connect(sender=export_user_data_task)
def task_success_handler(sender, result, **kwargs):
    print("Task succeeded")
    print("Sender: ", sender)
    print("Result: ", result)
    print(kwargs)


@task_failure.connect(sender=export_user_data_task)
def task_failure_handler(sender, result, **kwargs) -> None:
    print("Task failed")
    print("Sender: ", sender)
    print("Result: ", result)
    print(kwargs)
