"""Configuration settings for the translation application."""
import os
from pathlib import Path

# Model configuration
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model/transformer-model")
MAX_LENGTH = int(os.getenv("MAX_LENGTH", "50"))
NUM_BEAMS = int(os.getenv("NUM_BEAMS", "4"))

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# TensorFlow configuration
os.environ['TF_USE_LEGACY_KERAS'] = '1'

