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
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/2"

# ---------------------------
# Keep secret key consistent
# ---------------------------
SECRET_KEY = os.environ.get("SUPERSET_SECRET_KEY", "please-change-me")
