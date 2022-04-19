import os
import pybreaker
from conf import config


env = os.getenv("ENV", "development")
db_breaker = pybreaker.CircuitBreaker(
    fail_max=config[env].CIRCUIT_BREAKER_FAILURE_MAX,
    reset_timeout=config[env].CIRCUIT_BREAKER_RESET_TIMEOUT,
)
