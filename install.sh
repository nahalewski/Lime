#!/bin/bash

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Build Docker image
sudo docker build -t music-server .

# Stop existing container if it exists
sudo docker stop music-server || true
sudo docker rm music-server || true

# Create persistent volume for uploads
sudo docker volume create music-uploads

# Run container
sudo docker run -d \
    --name music-server \
    -p 5000:5000 \
    -v music-uploads:/app/uploads \
    --restart unless-stopped \
    music-server

echo "Music server installed and running on port 5000" 