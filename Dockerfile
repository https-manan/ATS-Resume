FROM python:3.11-slim

# System dependencies:
# - libmagic1: required by python-magic
# - WeasyPrint's rendering stack: pango, cairo, gdk-pixbuf, fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install Python dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models at build time
RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_sm

# Copy the app code (bert_fineTuned_model is no longer part of this repo —
# the model is now called remotely via the Hugging Face Inference API)
COPY . .

# Render/Railway both inject PORT dynamically at runtime
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}