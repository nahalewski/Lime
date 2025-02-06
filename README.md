# Lime Music Server & iOS App

A modern music streaming solution with YouTube download capabilities. This project consists of two main components:

1. A Flask-based music server that handles:
   - Music file storage and streaming
   - YouTube video downloads and conversion to MP3
   - RESTful API for client communication
   - Cookie-based YouTube authentication

2. An iOS client app (Lime) that provides:
   - Music library browsing and playback
   - YouTube download integration with authentication
   - Modern UI with portrait and landscape support
   - Background audio playback
   - Persistent authentication state

## Features

- **Music Library**
  - Stream your music collection from anywhere
  - Upload local music files
  - Background playback support
  - Progress tracking
  - Modern playback controls

- **YouTube Integration**
  - Download videos as MP3s
  - Automatic metadata extraction
  - Thumbnail embedding
  - Authentication support for age-restricted videos
  - Persistent login state

- **Modern UI**
  - Clean, responsive design
  - Dark mode support
  - Portrait and landscape layouts
  - Native iOS design patterns
  - Real-time status updates

## Server Requirements

- Python 3.8+
- FFmpeg
- Required Python packages (see `requirements.txt`)
- 100MB+ free storage for music files

## Server Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/lime-music.git
cd lime-music
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
- Active Apple Developer account for installation

## iOS App Installation

1. Open `Lime.xcodeproj` in Xcode
2. Update the `Configuration.swift` file with your server URL
3. Select your target device
4. Build and run the project

## Configuration

### Server Configuration
- The server stores data in two main directories:
  - `/data`: Database and cookies
  - `/uploads`: Music files
- Both directories are created automatically
- Configure the port in `app.py` if needed

### iOS Configuration
- Update `Configuration.swift` with your server URL:
```swift
enum Configuration {
    static let serverURL = "http://your-server-ip:5000"
}
```

## Security Notes

- The server uses cookie-based authentication for YouTube
- Cookies are stored securely and verified on each request
- HTTPS is recommended for production use
- The iOS app uses secure cookie storage

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

## License

MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube download functionality
- [Flask](https://flask.palletsprojects.com/) for the server framework
- [SwiftUI](https://developer.apple.com/xcode/swiftui/) for the iOS UI framework 