# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.10.5
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

COPY llm/requirements.txt ./llm/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r llm/requirements.txt

COPY utils/ ./utils/
RUN pip install --no-cache-dir -r utils/requirements.txt

COPY llm/ ./llm/

USER appuser

CMD ["gunicorn", "llm.app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "240", "--bind", "0.0.0.0:8000"]
