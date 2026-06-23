# Use Python 3.10 slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    curl \
    wget \
    git \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories
RUN mkdir -p /app/kelvin_data \
    /app/kelvin_uploads \
    /app/backups \
    /app/logs \
    /app/temp

# Copy application code
COPY . .

# Create volume for persistent data
VOLUME ["/app/kelvin_data", "/app/kelvin_uploads", "/app/backups", "/app/logs"]

# Expose port for Flask
EXPOSE 8080

# Set environment variables (ဒါတွေကို Railway/Platform ကနေ ထည့်ပေးရမယ်)
ENV PORT=8080

# Run the bot
CMD ["python", "main.py"]