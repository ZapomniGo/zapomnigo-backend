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
## How to start development server: 
By default, it is running on port 5000.
```bash
cd src/ && flask run --debug
```