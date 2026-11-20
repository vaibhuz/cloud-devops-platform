
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies
COPY app/requirements.txt .

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Upgrade vulnerable Python packages and setuptools
RUN pip install --no-cache-dir --upgrade \
    setuptools \
    jaraco.context==6.1.0 \
    wheel==0.46.2

# Copy application code
COPY app/ .

# Application port
EXPOSE 5000

# Start Flask application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]

