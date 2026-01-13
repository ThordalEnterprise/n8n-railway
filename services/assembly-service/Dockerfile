# Assembly Service - FREE (FFmpeg)
FROM python:3.11-slim

WORKDIR /app

# Install FFmpeg and dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service
COPY main.py .

# Create directories
RUN mkdir -p /tmp/assembly_output /tmp/assembly_temp

# Expose port
EXPOSE 8004

# Run service
CMD ["python", "main.py"]
