FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create uploads directory and data directory, set permissions
RUN mkdir -p uploads data && \
    chmod 777 uploads data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV SQLALCHEMY_DATABASE_URI=sqlite:///data/music.db

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--log-level", "debug", "--access-logfile", "-", "--error-logfile", "-", "app:app"] 