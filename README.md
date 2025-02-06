# Music Server

A modern web-based music server that allows you to upload and manage your music collection. Built with Flask and a modern web interface.

## Features

- Drag and drop multiple file upload
- Modern web interface
- Audio file streaming
- Music library management
- Docker support for easy deployment
- Persistent storage for uploaded files

## Requirements

- Ubuntu Server
- Docker (automatically installed by the installation script)
- Port 5000 available

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd music-server
```

2. Make the installation script executable:
```bash
chmod +x install.sh
```

3. Run the installation script:
```bash
./install.sh
```

The script will:
- Install Docker if not already installed
- Build the Docker image
- Create a persistent volume for uploads
- Start the container

## Manual Installation

If you prefer to install manually:

1. Install dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip libmagic1
pip3 install -r requirements.txt
```

2. Run the server:
```bash
python3 app.py
```

## Usage

1. Access the web interface at `http://your-server-ip:5000`
2. Upload music files by dragging and dropping them into the upload area
3. Manage your music library using the web interface

## Security Notes

- The server runs on port 5000 by default
- Consider setting up HTTPS if exposing to the internet
- Configure firewall rules as needed

## License

MIT License 