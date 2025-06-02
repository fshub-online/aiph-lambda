FROM python:3.13-alpine

WORKDIR /app

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy Alembic configuration and scripts
# Assumes alembic.ini and the 'alembic' directory are in the root of the build context (./backend)
COPY alembic.ini .
COPY alembic ./alembic

# Copy application code
COPY app ./app

# Ensure log directory exists for logging
RUN mkdir -p /app/log

# Expose port (default FastAPI/uvicorn port)
EXPOSE 8001

# Run Alembic migrations and then start the app
CMD alembic upgrade head && gunicorn -w 1 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001 app.main:app