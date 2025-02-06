# Lime Music Server & iOS App

A modern music streaming solution with YouTube download capabilities. This project consists of two main components:

1. A Flask-based music server that handles:
   - Music file storage and streaming
   - YouTube video downloads and conversion to MP3
   - RESTful API for client communication

2. An iOS client app (Lime) that provides:
   - Music library browsing and playback
   - YouTube download integration
   - Modern UI with portrait and landscape support
   - Background audio playback

## Server Requirements

- Python 3.8+
- FFmpeg
- Required Python packages (see `requirements.txt`)

## Server Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd [repo-name]
```

2. Install FFmpeg:
```bash
# On macOS with Homebrew
brew install ffmpeg

# On Ubuntu/Debian
sudo apt-get install ffmpeg
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## Docker Support

Build and run with Docker:

```bash
docker build -t music-server .
docker run -d \
    --name music-server \
    -p 5000:5000 \
    -v music-uploads:/app/uploads \
    -v music-data:/app/data \
    --restart unless-stopped \
    music-server
```

## iOS App Requirements

- iOS 16.0+
- Xcode 15.0+
- Swift 5.9+

## Features

- Stream music from your personal server
- Download music from YouTube
- Beautiful, responsive UI
- Portrait and landscape support
- Background playback
- Progress tracking
- Modern iOS design patterns

## License

[Your chosen license]

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 