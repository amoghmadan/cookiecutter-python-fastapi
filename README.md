# Cookiecutter FastAPI

Use this template to create a FastAPI Python project.

## How to use?

- Set-up base.
  ```bash
  cookiecutter https://github.com/amoghmadan/cookiecutter-python-fastapi.git
  ```
- Follow the prompts to customize your project.
  ```
  [1/5] package_name (app): play
  [2/5] package_name (app): play
  [3/5] project_description (Example application): Play with cookie cutter.
  [4/5] author_name (Your Name): Your Name
  [5/5] author_email (your@email.com): your@email.com
  ```

## Set-up?

- Initialize Git, it is very important for the project to work.
  ```bash
  git init -b main
  ```
- Install the dependencies.
  ```bash
  uv sync
  ```

## How to run?

- Run the server.
  ```bash
  {{package_name}} runserver
  ```
- Load JSON data (fixtures) into your models.
  ```bash
  {{package_name}} loaddata <file>.json
  ```
- Run the python shell (with application context).
  ```bash
  {{package_name}} shell
  ```
