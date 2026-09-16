FROM python:3.14-slim-trixie AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# setuptools_scm reads git tags to derive the version
RUN apt-get update \
    && apt-get install --no-install-recommends -y git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ARG HOME=/home/{{cookiecutter.package_name}}

WORKDIR /build

ENV UV_PROJECT_ENVIRONMENT=$HOME/.venv

# Install dependencies first (cached layer)
COPY pyproject.toml uv.lock ./
RUN mkdir -p "$HOME" && uv sync --frozen --no-dev --no-install-project

# Install the project itself
COPY src/ src/
RUN uv sync --frozen --no-dev --no-editable


# --- Runtime stage ---
FROM python:3.14-slim-trixie AS runtime

ARG USERNAME={{cookiecutter.package_name}}
ARG HOME=/home/$USERNAME

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd -r "$USERNAME" \
    && useradd -r -g "$USERNAME" -m -d "$HOME" "$USERNAME"

WORKDIR "$HOME/{{cookiecutter.package_name}}"
RUN chown -R "$USERNAME":"$USERNAME" "$HOME"

USER "$USERNAME"

ENV PATH="$HOME/.venv/bin:$PATH"

# Installed application and its dependencies
COPY --from=builder --chown="$USERNAME":"$USERNAME" /home/$USERNAME/.venv "$HOME/.venv"

# Project source (fixtures, migrations, etc.) matching the dev layout
COPY --chown="$USERNAME":"$USERNAME" src/ src/

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/ping/', timeout=5)"]

CMD ["uvicorn", "{{cookiecutter.package_name}}.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]
