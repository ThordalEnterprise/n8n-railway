# Video Service - FREE (ComfyUI Client)
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy service
COPY main.py .

# Create output directory
RUN mkdir -p /tmp/video_output

# Expose port
EXPOSE 8003

# Run service
CMD ["python", "main.py"]
