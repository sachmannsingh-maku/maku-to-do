FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

COPY pyproject.toml poetry.lock* .


COPY maku_todo ./maku_todo

RUN poetry install --no-root

copy alembic.ini .

EXPOSE 8000

CMD ["sh", "-c", "poetry run alembic upgrade head && poetry run uvicorn maku_todo.main:app --host 0.0.0.0 --port 8000"]

#CMD ["poetry", "run","alembic", "upgrade", "head", "&&", "uvicorn", "maku_todo.main:app", "--host", "0.0.0.0", "--port", "8000"]