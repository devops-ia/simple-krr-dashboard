#!/bin/sh
set -e

# Override access log based on DISABLE_HTTP_LOGS
if [ "${DISABLE_HTTP_LOGS}" = "true" ]; then
    GUNICORN_ACCESS_LOG="/dev/null"
fi

# Execute gunicorn with environment variables
exec gunicorn \
    --bind "${GUNICORN_BIND}" \
    --workers "${GUNICORN_WORKERS}" \
    --threads "${GUNICORN_THREADS}" \
    --worker-class "${GUNICORN_WORKER_CLASS}" \
    --worker-tmp-dir "${GUNICORN_WORKER_TMP_DIR}" \
    --timeout "${GUNICORN_TIMEOUT}" \
    --graceful-timeout "${GUNICORN_GRACEFUL_TIMEOUT}" \
    --keep-alive "${GUNICORN_KEEPALIVE}" \
    --log-level "${GUNICORN_LOG_LEVEL}" \
    --access-logfile "${GUNICORN_ACCESS_LOG}" \
    --error-logfile "${GUNICORN_ERROR_LOG}" \
    "simple_krr_dashboard.main:create_app()"
