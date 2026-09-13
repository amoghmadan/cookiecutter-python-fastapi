# {{cookiecutter.package_name}}

{{cookiecutter.package_name}} API

## Prerequisites

- Python 3.14
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
cp .env.example .env
uv sync --dev
```

## How to run a development server?

```bash
python -m {{cookiecutter.package_name}} runserver
```

## Migrations

- Make migration files

  ```bash
  uv run alembic revision --autogenerate -m "Your message here"
  ```

- Migrate

  ```bash
  uv run alembic upgrade head
  ```

## How to load fixtures?

Place JSON fixture files in a `fixtures/` directory at the project root, then run:

```bash
python -m {{cookiecutter.package_name}} loaddata --files <file>.json
```

## How to run Python REPL?

```bash
python -m {{cookiecutter.package_name}} shell
```

Inline commands are also supported:

```bash
python -m {{cookiecutter.package_name}} shell --command "from {{cookiecutter.package_name}}.db import session; print(session)"
```

## Quality checks

- Format code with Ruff

  ```bash
  uv run ruff format .
  ```

- Lint code with Ruff

  ```bash
  uv run ruff check .
  ```

- Type check with ty

  ```bash
  uv run ty check
  ```

- Scan for security vulnerabilities with Bandit

  ```bash
  uv run bandit -c pyproject.toml -r src
  ```

- Run tests

  ```bash
  uv run pytest
  ```

- Run tests with coverage report

  ```bash
  uv run pytest --cov={{cookiecutter.package_name}}
  ```

## How to build an image for deployment?

```bash
docker build -t {{cookiecutter.package_name}}:$(uv run python -c "from {{cookiecutter.package_name}} import __version__; print(__version__)") .
```

Run with Docker Compose:

```bash
TAG=latest docker compose up
```
