# Dockerfile for Railway deployment
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
COPY frontend /app/frontend

EXPOSE 8000

# Start FastAPI directly using Railway's PORT
CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"

