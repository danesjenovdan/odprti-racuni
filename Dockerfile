FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gettext && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
	UV_LINK_MODE=copy \
	UV_PYTHON_DOWNLOADS=0 \
	UV_PROJECT_ENVIRONMENT=/opt/venv \
	PATH="/opt/venv/bin:$PATH"

# Install dependencies first (cached separately from app code changes).
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked --no-dev --no-install-project

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
	uv sync --locked --no-dev

RUN python3 manage.py compilemessages

FROM python:3.14-slim AS runtime

WORKDIR /app

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
	PATH="/opt/venv/bin:$PATH" \
	DJANGO_SETTINGS_MODULE=ppp.settings

COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /app /app

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
