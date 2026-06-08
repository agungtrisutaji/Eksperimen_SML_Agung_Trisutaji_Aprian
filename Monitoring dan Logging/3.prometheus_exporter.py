from __future__ import annotations

import os
import time

import psutil
import requests
from prometheus_client import Gauge, start_http_server


API_URL = os.getenv("PREDICTION_API_URL", "http://127.0.0.1:8000")
EXPORTER_PORT = int(os.getenv("EXPORTER_PORT", "8001"))
SCRAPE_INTERVAL_SECONDS = int(os.getenv("EXPORTER_INTERVAL_SECONDS", "5"))

model_api_health_status = Gauge(
    "model_api_health_status", "Health status of the FastAPI model service."
)
model_api_loaded_status = Gauge(
    "model_api_loaded_status", "Loaded status reported by the FastAPI model service."
)
model_api_response_latency_seconds = Gauge(
    "model_api_response_latency_seconds", "Latency of the /health endpoint in seconds."
)
system_cpu_percent = Gauge("system_cpu_percent", "System CPU utilization percent.")
system_memory_percent = Gauge("system_memory_percent", "System memory utilization percent.")


def collect_health() -> None:
    started = time.perf_counter()
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        payload = response.json()
        model_api_health_status.set(1 if payload.get("status") == "ok" else 0)
        model_api_loaded_status.set(1 if payload.get("model_loaded") else 0)
    except Exception:
        model_api_health_status.set(0)
        model_api_loaded_status.set(0)
    finally:
        model_api_response_latency_seconds.set(time.perf_counter() - started)


def collect_system() -> None:
    system_cpu_percent.set(psutil.cpu_percent(interval=None))
    system_memory_percent.set(psutil.virtual_memory().percent)


def main() -> None:
    start_http_server(EXPORTER_PORT)
    print(f"Prometheus exporter is running on port {EXPORTER_PORT}")
    print(f"Checking API health at {API_URL}/health")
    while True:
        collect_health()
        collect_system()
        time.sleep(SCRAPE_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()

