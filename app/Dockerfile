# Use official Python base image
FROM python:3.13-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    netcat-openbsd curl && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -u 1001 -r -s /sbin/nologin flask-user

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code and templates
COPY . .

# Ensure log directory exists (optional, since K8s mounts it)
RUN mkdir -p /var/log/flask && chown -R 1001:1001 /var/log/flask

# Switch to non-root user
USER 1001

# Expose Flask port
EXPOSE 5000

# Unbuffered output for K8s logs
CMD ["python", "-u", "app.py"]