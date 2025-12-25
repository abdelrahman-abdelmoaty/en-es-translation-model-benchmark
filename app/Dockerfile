# Dockerfile for Railway deployment (combines backend + nginx)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TF_USE_LEGACY_KERAS=1

# Install system dependencies including git and git-lfs
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    nginx \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Initialize git-lfs
RUN git lfs install

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create model directory
RUN mkdir -p /app/model

# Copy entire app directory first (to get .git if available for LFS)
COPY . /tmp/repo

# Pull Git LFS files if .git exists, otherwise copy model directory
RUN if [ -d /tmp/repo/.git ]; then \
      cd /tmp/repo && \
      git lfs install && \
      git lfs pull && \
      cp -r transformer-model /app/model/transformer-model; \
    else \
      echo "No .git found, copying model files directly"; \
      cp -r /tmp/repo/transformer-model /app/model/transformer-model || \
      (echo "ERROR: Model files not found. Listing:" && ls -la /tmp/repo/ && exit 1); \
    fi

# Verify critical model files exist and have content
RUN echo "Verifying model files..." && \
    ls -lh /app/model/transformer-model/ && \
    if [ ! -f /app/model/transformer-model/tokenizer_config.json ] || [ ! -s /app/model/transformer-model/tokenizer_config.json ]; then \
      echo "ERROR: tokenizer_config.json missing or empty"; \
      exit 1; \
    fi && \
    if [ ! -f /app/model/transformer-model/tf_model.h5 ]; then \
      echo "ERROR: tf_model.h5 missing"; \
      exit 1; \
    fi && \
    MODEL_SIZE=$(stat -c%s /app/model/transformer-model/tf_model.h5 2>/dev/null || echo 0) && \
    if [ "$MODEL_SIZE" -lt 1000000 ]; then \
      echo "ERROR: tf_model.h5 too small ($MODEL_SIZE bytes), likely LFS pointer"; \
      head -c 200 /app/model/transformer-model/tf_model.h5; \
      exit 1; \
    fi && \
    echo "Model files verified successfully"

# Copy application code
COPY backend/app /app/app

# Copy frontend
COPY frontend /usr/share/nginx/html

# Remove default nginx site
RUN rm -f /etc/nginx/sites-enabled/default

# Copy nginx config
COPY nginx.render.conf /etc/nginx/conf.d/default.conf

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
PORT=${PORT:-80}\n\
# Update nginx to listen on Railway PORT\n\
sed -i "s/listen 80/listen $PORT/" /etc/nginx/conf.d/default.conf\n\
# Test nginx config\n\
nginx -t\n\
# Start FastAPI in background\n\
echo "Starting FastAPI..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/fastapi.log 2>&1 &\n\
FASTAPI_PID=$!\n\
# Wait for FastAPI to be ready (check health endpoint)\n\
echo "Waiting for FastAPI to start..."\n\
for i in {1..60}; do\n\
  if curl -f http://localhost:8000/health > /dev/null 2>&1; then\n\
    echo "FastAPI is ready!"\n\
    break\n\
  fi\n\
  if [ $i -eq 60 ]; then\n\
    echo "FastAPI failed to start after 60 seconds. Logs:"\n\
    cat /tmp/fastapi.log\n\
    exit 1\n\
  fi\n\
  sleep 1\n\
done\n\
# Start nginx in foreground\n\
echo "Starting nginx..."\n\
exec nginx -g "daemon off;"' > /start.sh && chmod +x /start.sh

EXPOSE 80 8000

CMD ["/start.sh"]

