FROM python:3.14-alpine AS builder

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy --ignore-pipfile

FROM alpine/kubectl:1.35.1 AS kubectl

FROM python:3.14-alpine

LABEL org.opencontainers.image.title="Simple KRR Dashboard" \
      org.opencontainers.image.description="KRR dashboard visualization" \
      org.opencontainers.image.authors="ialejandro" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/devops-ia/simple-krr-dashboard"

RUN apk add --no-cache \
    libffi \
    tini

WORKDIR /app

COPY --from=kubectl /usr/local/bin/kubectl /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin/gunicorn /usr/local/bin/gunicorn
COPY --chmod=755 docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
COPY src/ ./src/

RUN adduser -D -u 1000 krr && \
    mkdir -p /reports && \
    chown -R krr:krr /app /reports

USER krr

STOPSIGNAL SIGTERM

EXPOSE 8080

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    GUNICORN_BIND=0.0.0.0:8080 \
    GUNICORN_WORKERS=2 \
    GUNICORN_THREADS=4 \
    GUNICORN_WORKER_CLASS=gthread \
    GUNICORN_WORKER_TMP_DIR=/dev/shm \
    GUNICORN_TIMEOUT=30 \
    GUNICORN_GRACEFUL_TIMEOUT=30 \
    GUNICORN_KEEPALIVE=5 \
    GUNICORN_LOG_LEVEL=error \
    GUNICORN_ACCESS_LOG=- \
    GUNICORN_ERROR_LOG=- \
    DISABLE_HTTP_LOGS=false \
    LOG_OUTPUT_FORMAT=text

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["docker-entrypoint.sh"]
