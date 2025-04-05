FROM python:3.13-alpine

LABEL org.opencontainers.image.title="Simple KRR Dashboard" \
      org.opencontainers.image.description="KRR dashboard visualization" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.created="2024-04-11" \
      org.opencontainers.image.authors="ialejandro" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.base.name="python:3.13-alpine"

WORKDIR /app

COPY src/ Pipfile Pipfile.lock ./
RUN pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy

RUN adduser -D -u 1000 krr && \
    mkdir -p /reports      && \
    chown -R krr:krr /app /reports

USER krr

EXPOSE 8080

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "simple_krr_dashboard.main:create_app()"]
