FROM python:3.11-slim

# System dependencies:
# - libmagic1: required by python-magic
# - WeasyPrint's rendering stack: pango, cairo, gdk-pixbuf, fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# Install Python dependencies first (better layer caching —
# this layer only rebuilds when requirements.txt changes, not on every code edit)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models at build time, not runtime —
# avoids a slow first-request and avoids needing internet access from the running container
RUN python -m spacy download en_core_web_md
RUN python -m spacy download en_core_web_sm

# Copy the rest of the app — this includes your bert_fineTuned_model folder
COPY . .

# Railway assigns PORT dynamically at runtime — this must NOT be hardcoded
CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}