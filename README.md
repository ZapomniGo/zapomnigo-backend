# Python API

## Prerequisites

Check your python version. This project runs on 3.11.4:

```bash
python --version
```

If you do not have it, you can use a tool such as `pyenv` to install it.
How to install pyenv on:

* [Linux](https://brain2life.hashnode.dev/how-to-install-pyenv-python-version-manager-on-ubuntu-2004)
* [MacOS](https://gist.github.com/josemarimanio/9e0c177c90dee97808bad163587e80f8)

```bash 
pyenv install 3.11.4
```

## How to set up project:

1. Run `poetry config virtualenvs.in-project true`
2. If you have pyenv installed run `poetry config virtualenvs.prefer-active-python true`
3. To activate your python virtualenv run `poetry shell`
4. Run `poetry install`

## How to add new python packages

```bash
poetry add package-name
```
## Redis

To run redis locally do:
```bash
docker run -d --name local-redis -p 6379:6379 redis:latest
```

## How to start development server:

By default, it is running on port 3884.

```bash
poetry run start
```

# Working with migrations

### If you have never created migrations and you don't have the migrations folder:

1. Run `export FLASK_APP=main:create_app` or add it to your .bashrc/.zshrc file
2. Run `flask db init` in the `/src` folder

### If you are working with an exsisting state of the database or existing migrations

1. Run `flask db stamp head` this indicates that the current state of the database represents the application of all
   migrations.

### Making changes to the tables

* Make changes to the classes located in the `/database/models` folder
* After you have made a change do:

```bash
flask db migrate -m "Migration message"
```

* To apply the changes described by the migration script to the database do:

```bash
flask db upgrade
```

## Celery

We use Celery to execute background tasks such as sending emails, extracting the user data, and other long-running
tasks.

The Celery worker is responsible for executing tasks that are added to the task queue.
The Celery Beat service is a scheduler that sends tasks to the worker at regular intervals
In order fo Celery to execute tasks both immediately and on a schedule, both services should be running concurrently.

```bash
celery -A "src.celery_task_queue.make_celery" worker --autoscale=8,1 --loglevel INFO
celery -A "src.celery_task_queue.make_celery" beat --loglevel INFO
```
