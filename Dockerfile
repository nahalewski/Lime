FROM ubuntu:22.04

# Prevent tzdata questions during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y \
        python3.9 \
        python3-pip \
        python3-dev \
        build-essential \
        libmagic1 \
        ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Verify ffmpeg installation
RUN ffmpeg -version

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

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