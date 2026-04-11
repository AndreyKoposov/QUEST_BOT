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

COPY vk_bot/requirements.txt ./vk_bot/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r vk_bot/requirements.txt

COPY core/ ./core/
RUN pip install --no-cache-dir -r core/requirements.txt

COPY utils/ ./utils/
RUN pip install --no-cache-dir -r utils/requirements.txt

COPY vk_bot/ ./vk_bot/

USER appuser

CMD ["python", "-m", "vk_bot"]
