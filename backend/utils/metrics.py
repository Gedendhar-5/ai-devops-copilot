import random
from typing import TypedDict


class SimulatedMetrics(TypedDict):
    cpu: str
    memory: str
    error_rate: str


SCENARIOS = [
    {"cpu": "92%", "memory": "78%", "error_rate": "34%"},
    {"cpu": "45%", "memory": "91%", "error_rate": "5%"},
    {"cpu": "21%", "memory": "30%", "error_rate": "67%"},
    {"cpu": "88%", "memory": "85%", "error_rate": "22%"},
    {"cpu": "12%", "memory": "15%", "error_rate": "2%"},
]

SAMPLE_LOGS = [
    "ERROR: Connection timeout after 30s. Service: payment-api. Pod: payment-7f9d-xkz2p",
    "CRITICAL: Out of memory. Killed process: auth-service. Node: node-02",
    "ERROR: 503 Service Unavailable. Upstream: order-service. Retries: 5",
    "WARN: CPU throttling detected. Container: recommendation-engine. Limit: 500m",
    "ERROR: Database connection pool exhausted. Service: user-api. Pool size: 10",
]


def get_simulated_metrics() -> SimulatedMetrics:
    """Returns a random simulated metric scenario."""
    return random.choice(SCENARIOS)


def get_sample_log() -> str:
    """Returns a random sample log line for demo purposes."""
    return random.choice(SAMPLE_LOGS)