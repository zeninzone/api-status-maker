FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p /app/database /app/config \
    && chmod -R 777 /app/database

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV PYTHONPATH=/app

# Expose port
EXPOSE 5000

# Run the application
CMD ["flask", "run"]
