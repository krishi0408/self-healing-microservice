from fastapi import FastAPI, Response
import random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = FastAPI()

# Prometheus Metrics
REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])
FAILURES = Counter("app_failures_total", "Total failures", ["endpoint"])

@app.get("/predict")
def predict():
    start_time = time.time()
    endpoint = "/predict"
    try:
        if random.random() < 0.2:  # 20% simulated failure
            FAILURES.labels(endpoint=endpoint).inc()
            raise Exception("Simulated failure")

        REQUEST_COUNT.labels(endpoint=endpoint).inc()
        return {"prediction": "success"}

    finally:
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(time.time() - start_time)

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)