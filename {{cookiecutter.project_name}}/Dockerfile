FROM python:3.14-slim-trixie AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# setuptools_scm reads git tags to derive the version
RUN apt-get update \
    && apt-get install --no-install-recommends -y git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy the full project (minus .dockerignore) so the version can be derived
COPY . .

# Build the venv at the same absolute path the runtime stage will use,
# so script shebangs (e.g. /home/{{cookiecutter.package_name}}/.venv/bin/python) stay valid.
ARG HOME=/home/{{cookiecutter.package_name}}
ARG VENV_PATH=$HOME/.venv
RUN mkdir -p "$HOME" \
    && python3 -m venv "$VENV_PATH" \
    && "$VENV_PATH/bin/pip" install --no-cache-dir .


# --- Runtime stage ---
FROM python:3.14-slim-trixie AS runtime

ARG USERNAME={{cookiecutter.package_name}}
ARG HOME=/home/$USERNAME
ARG VENV_PATH=$HOME/.venv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_INPUT=1

RUN groupadd -r "$USERNAME" \
    && useradd -r -g "$USERNAME" -m -d "$HOME" "$USERNAME"

WORKDIR "$HOME/{{cookiecutter.package_name}}"
RUN chown -R "$USERNAME":"$USERNAME" "$HOME"

USER "$USERNAME"

ENV PATH="$VENV_PATH/bin:$PATH"

# Installed application and its dependencies
COPY --from=builder --chown="$USERNAME":"$USERNAME" "$VENV_PATH" "$VENV_PATH"

# Project source (fixtures, migrations, etc.) matching the dev layout
COPY --chown="$USERNAME":"$USERNAME" . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/v1/ping/', timeout=5)"]

CMD ["uvicorn", "{{cookiecutter.package_name}}.asgi:application", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--log-level", "info"]
