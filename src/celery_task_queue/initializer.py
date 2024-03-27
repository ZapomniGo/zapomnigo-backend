from celery import Celery, Task
from flask import Flask


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'],
                        task_cls=FlaskTask, broker_connection_retry_on_startup=True, broker_connection_max_retries=10)
    celery_app.set_default()
    app.extensions["celery"] = celery_app

    return celery_app
