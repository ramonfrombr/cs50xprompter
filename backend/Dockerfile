# ============================================
# Base image
# ============================================
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production \
    FLASK_APP=wsgi.py

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv/poetry if needed
RUN pip install --upgrade pip

# Copy dependencies first (for caching)
COPY requirements.txt .

# Install dependencies (with eventlet for SocketIO)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# ============================================
# Run the app with eventlet (SocketIO friendly)
# ============================================
CMD ["python", "wsgi.py"]
