FROM python:3.11.0-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/static /app/media /app/staticfiles

# Set permissions
RUN chmod -R 755 /app

# Expose port
EXPOSE 8000

# Start the application directly
CMD ["gunicorn", "care_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]