# Dockerfile — robust pip bootstrap + installs for Superset image
FROM apache/superset:latest

USER root

ENV PKGS="psycopg2-binary pymysql gevent mysqlclient"

# Try to install into /app/.venv if present; otherwise use system python3.
# Use ensurepip to bootstrap pip if needed. Fall back to apt-get install python3-pip when ensurepip is not available.
RUN set -eux; \
    # install build deps required for mysqlclient and Python headers
    apt-get update; \
    apt-get install -y --no-install-recommends \
      build-essential \
      default-libmysqlclient-dev \
      python3-dev \
      pkg-config \
      libssl-dev \
      ca-certificates \
      && rm -rf /var/lib/apt/lists/*; \
    \
    if [ -x /app/.venv/bin/python3 ]; then \
      PY=/app/.venv/bin/python3; \
    elif command -v python3 >/dev/null 2>&1; then \
      PY=python3; \
    else \
      PY=python; \
    fi; \
    echo "Using python at: $PY"; \
    # Ensure pip exists for that python
    if "$PY" -m pip --version >/dev/null 2>&1; then \
      echo "pip already available for $PY"; \
    else \
      echo "Bootstrapping pip for $PY"; \
      if "$PY" -m ensurepip --upgrade >/dev/null 2>&1; then \
        true; \
      else \
        echo "ensurepip not available; installing python3-pip via apt-get"; \
        apt-get update && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*; \
      fi; \
    fi; \
    # Upgrade pip and install packages into the same interpreter
    "$PY" -m pip install --no-cache-dir --upgrade pip setuptools wheel; \
    "$PY" -m pip install --no-cache-dir $PKGS; \
    # show versions for quick debug
    "$PY" -m pip freeze | grep -E "psycopg2|pymysql|gevent" || true

# revert to expected runtime user
USER superset
