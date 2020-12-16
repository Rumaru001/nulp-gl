#Lab 1
I used ```pyenv``` and ```poetry```.
Python version 3.6.8

If you want to watch source code, click [here](main.py)

There are some steps that you want to do:

- Install current version of python via pyenv:
```
pyenv install 3.6.8
```

- Install poetry:

```
pip install poetry
```

- Install virtual environment
```
poetry use env 3.6.8
poetry use env [path]
```

- Install packages
```
poetry install
poetry shell
```

- Activate virtual environment
```
source activate
```
or
```
cd path/to/your/virtual/environment/Scripts
activate
```

- Run server:

```
poetry run python wsgi.py
```

- Make migrations
```
path/to/venv/Scripts/alembic.exe revision --autogenerate
```
or
```
alembic revision --autogenerate
```
```
alembic upgrade head
```