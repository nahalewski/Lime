FROM python:3.9-bullseye

WORKDIR /app

# Install system dependencies including ffmpeg
RUN apt-get update && \
    apt-get install -y \
        libmagic1 \
        ffmpeg \
        python3-dev \
        build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Verify ffmpeg installation
RUN ffmpeg -version

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create uploads and data directories with proper permissions
RUN mkdir -p /app/uploads /app/data && \
    chmod 777 /app/uploads /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV SQLALCHEMY_DATABASE_URI=sqlite:///data/music.db

# Copy application files
COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "app:app"] 