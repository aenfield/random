FROM python:3.11-slim

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# copy the application into the container
COPY . /app

# install application dependencies
WORKDIR /app
RUN uv sync --frozen --no-cache

# and run the app
CMD ["/app/.venv/bin/gunicorn", "-b", "0.0.0.0:8080", "first-app:app"]
#CMD ["/app/.venv/bin/flask", "run", "app/first-app.py", "--host=0.0.0.0", "--port=8080"]


#CMD ["/app/.venv/bin/flask", "run", "app/first-app.py", "--port", "80", "--host", "0.0.0.0"]


# FROM python:3.13 AS builder

# ENV PYTHONUNBUFFERED=1 \
#     PYTHONDONTWRITEBYTECODE=1
# WORKDIR /app

# RUN pip install poetry
# RUN poetry config virtualenvs.in-project true
# COPY pyproject.toml poetry.lock ./
# RUN poetry install --no-root
# FROM python:3.13-slim
# WORKDIR /app
# COPY --from=builder /app/.venv .venv/
# COPY . .
# CMD ["/app/.venv/bin/flask", "run", "--host=0.0.0.0", "--port=8080"]
