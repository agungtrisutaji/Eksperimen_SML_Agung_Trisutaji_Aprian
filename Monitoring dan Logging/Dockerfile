FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY ["Monitoring dan Logging/requirements.txt", "/app/Monitoring dan Logging/requirements.txt"]
RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -r "/app/Monitoring dan Logging/requirements.txt"

COPY ["Membangun_model", "/app/Membangun_model"]
COPY ["Monitoring dan Logging", "/app/Monitoring dan Logging"]

WORKDIR "/app/Monitoring dan Logging"

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

