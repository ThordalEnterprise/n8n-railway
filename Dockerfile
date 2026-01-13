# Use official n8n Docker image
FROM n8nio/n8n:latest

# Expose n8n web interface port
EXPOSE 5678

# The official n8n image already sets up:
# - User 'node' with correct permissions
# - Working directory /home/node/.n8n for data persistence
# - Entrypoint to start n8n

# Data will be persisted in /home/node/.n8n
# Mount a Railway volume to this path for data persistence
