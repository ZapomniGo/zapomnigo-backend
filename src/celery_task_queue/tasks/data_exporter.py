from typing import Dict, Any

from celery import shared_task, signature
from celery.result import AsyncResult
from celery.signals import task_success, task_failure

from src.config import SENDER_EMAIL
from src.database.repositories.users_repository import UsersRepository
from src.functionality.users_functionallity import UsersFunctionality
from src.celery_task_queue.tasks.mailer import send_email_background_task


@shared_task(ignore_result=False)
def export_user_data_task(user_id: str) -> Dict[str, Any]:
    user = UsersRepository.get_user_by_ulid(user_id)
    return {"user_data": UsersFunctionality.export_user_data(user)}


@task_success.connect
def export_user_data_success_handler(sender, result, *args, **kwargs):
    if sender.name == export_user_data_task.name:
        print(sender.request)
        task_id = sender.request.id
        task = AsyncResult(task_id)
        print(f"Task {sender.name} with id {task.task_id} succeeded")
        # TODO send data to s3 and send email link to the user


@task_failure.connect
def export_user_data_failure_handler(sender, task_id, exception, args, kwargs, traceback, einfo, **other_kwargs):
    if sender.name == export_user_data_task.name:
        message = f"Task {str(task_id)} failed with exception {str(exception)}!"
        signature(send_email_background_task, args=(SENDER_EMAIL, "User data export task failed", message)).apply_async()
