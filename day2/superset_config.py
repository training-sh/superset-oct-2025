# minimal superset_config.py
# SQLAlchemy connection for Superset metadata (Postgres)
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://superset:superset_pass@postgres:5432/superset"

# Optional - recommend later to set CACHE_CONFIG, CELERY configs, etc.
# SECRET_KEY can be set via env; SUPERSET_SECRET_KEY env is used above.

# superset_config.py
import os
from cachelib.redis import RedisCache

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# ---------------------------
# Query Results backend (SQL Lab / async results storage)
# ---------------------------
# Use Redis for results; cachelib RedisCache instance is fine.
RESULTS_BACKEND = RedisCache(
    host=REDIS_HOST,
    port=REDIS_PORT,
    key_prefix="superset_results",
)

# # ---------------------------
# # Flask / App cache (UI caches)
# # ---------------------------
# CACHE_CONFIG = {
#     "CACHE_TYPE": "redis",
#     "CACHE_DEFAULT_TIMEOUT": 300,
#     "CACHE_KEY_PREFIX": "superset_cache:",
#     "CACHE_REDIS_HOST": REDIS_HOST,
#     "CACHE_REDIS_PORT": REDIS_PORT,
#     "CACHE_REDIS_DB": 1,
# }

# # Superset data cache (some versions use DATA_CACHE_CONFIG)
# DATA_CACHE_CONFIG = {
#     "CACHE_TYPE": "redis",
#     "CACHE_DEFAULT_TIMEOUT": 300,
#     "CACHE_KEY_PREFIX": "superset_data_cache:",
#     "CACHE_REDIS_HOST": REDIS_HOST,
#     "CACHE_REDIS_PORT": REDIS_PORT,
#     "CACHE_REDIS_DB": 1,
# }

# ---------------------------
# Celery broker/result backend (defined but workers optional)
# ---------------------------
# You can leave these here; without workers tasks won't be processed.
from celery.schedules import crontab

CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"

class CeleryConfig:
    broker_url = CELERY_BROKER_URL
    result_backend = CELERY_RESULT_BACKEND
    timezone = "UTC"

CELERY_CONFIG = CeleryConfig

# ---------------------------
# Keep secret key consistent
# ---------------------------
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "please-change-me")


FEATURE_FLAGS = {"DASHBOARD_FILTERS_EXPERIMENTAL": True, "DASHBOARD_NATIVE_FILTERS_SET": True, "DASHBOARD_NATIVE_FILTERS": True, "DASHBOARD_CROSS_FILTERS": True, "ENABLE_TEMPLATE_PROCESSING": True}

# Task soft/hard time limits (in seconds)
CELERY_TASK_SOFT_TIME_LIMIT = 600    # soft limit (task can cleanup)
CELERY_TASK_TIME_LIMIT = 700         # hard limit (force kill)

# Optional: reduce concurrency to avoid resource exhaustion
CELERY_WORKER_CONCURRENCY = 8
