# Voice Service - FREE (Coqui TTS)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for audio processing
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service
COPY main.py .

# Create output directory
RUN mkdir -p /tmp/tts_output

# Expose port
EXPOSE 8002

# Run service
CMD ["python", "main.py"]
