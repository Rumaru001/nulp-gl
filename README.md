#Lab 1
I used ```pyenv``` and ```poetry```.
Python version 3.6.8

If you want to watch source code, click [here](main.py)

There are some steps that you want to use:

- Using pyenv install current version of python:
```
pyenv install 3.6.8
pyenv local 3.6.8
```

- Install poetry:

```
pip install poetry waitress
```

- Run server:

```
poetry run python wsgi.py
```