FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app/

COPY pyproject.toml poetry.lock /app/

RUN pip install --no-cache-dir -U pip poetry

RUN poetry config virtualenvs.create false
RUN poetry install --with dev --no-root --no-interaction --no-ansi

COPY . /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
