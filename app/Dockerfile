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

# Copy requirements and install Python dependencies (including huggingface-hub for model download)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt huggingface-hub

# Create model directory
RUN mkdir -p /app/model

# Copy model directory to check if files are LFS pointers
COPY transformer-model /tmp/model-check

# Check if model file is LFS pointer or actual file, download from Hugging Face if needed
RUN MODEL_SIZE=$(stat -c%s /tmp/model-check/tf_model.h5 2>/dev/null || echo 0) && \
    if [ "$MODEL_SIZE" -lt 1000000 ]; then \
      echo "Model file is LFS pointer ($MODEL_SIZE bytes) or missing"; \
      echo "Downloading model from Hugging Face..."; \
      python3 -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Helsinki-NLP/opus-mt-en-es', local_dir='/app/model/transformer-model', local_dir_use_symlinks=False)"; \
    else \
      echo "Model file is actual file ($MODEL_SIZE bytes), using local copy..."; \
      cp -r /tmp/model-check /app/model/transformer-model; \
    fi && \
    rm -rf /tmp/model-check

# Verify critical model files exist and are not LFS pointers
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
      echo "ERROR: tf_model.h5 is only $MODEL_SIZE bytes (expected ~300MB)"; \
      echo "This appears to be a Git LFS pointer file, not the actual model."; \
      echo "Railway needs to pull LFS files before building."; \
      echo "First 200 bytes of file:"; \
      head -c 200 /app/model/transformer-model/tf_model.h5; \
      echo ""; \
      echo "Please ensure Railway is configured to pull Git LFS files."; \
      exit 1; \
    fi && \
    echo "Model files verified successfully (tf_model.h5 size: $MODEL_SIZE bytes)"

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

