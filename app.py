import os
from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import magic
import logging
import yt_dlp
import re
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Ensure data and uploads directories exist with absolute paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
COOKIES_DIR = os.path.join(DATA_DIR, 'cookies')
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(COOKIES_DIR, exist_ok=True)

# Set permissions for directories
os.chmod(DATA_DIR, 0o777)
os.chmod(UPLOAD_DIR, 0o777)
os.chmod(COOKIES_DIR, 0o777)

# Configure app
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(DATA_DIR, "music.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# YouTube credentials file
YOUTUBE_COOKIES_FILE = os.path.join(COOKIES_DIR, 'youtube.json')

db = SQLAlchemy(app)

logger.info(f"Upload directory created at {UPLOAD_DIR}")
logger.info(f"Database path: {os.path.join(DATA_DIR, 'music.db')}")

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    artist = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'title': self.title,
            'artist': self.artist,
            'uploaded_at': self.uploaded_at.isoformat(),
        }

def allowed_file(filename):
    try:
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(filename)
        logger.info(f"File {filename} has MIME type: {file_type}")
        
        # Allow both audio files and M4A files (which might be detected as video/mp4)
        return file_type.startswith('audio/') or (
            file_type == 'video/mp4' and filename.lower().endswith('.m4a')
        )
    except Exception as e:
        logger.error(f"Error checking file type for {filename}: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        songs = Song.query.all()
        return jsonify([song.to_dict() for song in songs])
    except Exception as e:
        logger.error(f"Error fetching songs: {str(e)}")
        return jsonify({'error': 'Failed to fetch songs'}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'files[]' not in request.files:
            logger.warning("No file part in request")
            return jsonify({'error': 'No file part'}), 400
        
        files = request.files.getlist('files[]')
        uploaded_files = []
        
        for file in files:
            if file.filename == '':
                logger.warning("Empty filename submitted")
                continue
                
            if file:
                try:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    logger.info(f"Saving file to: {file_path}")
                    file.save(file_path)
                    
                    if not allowed_file(file_path):
                        logger.warning(f"File {filename} is not an allowed audio file")
                        os.remove(file_path)
                        continue
                        
                    song = Song(
                        filename=filename,
                        title=os.path.splitext(filename)[0],
                        file_path=file_path
                    )
                    db.session.add(song)
                    uploaded_files.append(filename)
                    logger.info(f"Successfully processed file: {filename}")
                except Exception as e:
                    logger.error(f"Error processing file {file.filename}: {str(e)}")
                    continue
        
        db.session.commit()
        logger.info(f"Successfully committed {len(uploaded_files)} files to database")
        return jsonify({
            'message': f'Successfully uploaded {len(uploaded_files)} files',
            'files': uploaded_files
        })
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/api/stream/<int:song_id>')
def stream_file(song_id):
    try:
        song = Song.query.get_or_404(song_id)
        return send_file(song.file_path)
    except Exception as e:
        logger.error(f"Error streaming song {song_id}: {str(e)}")
        return jsonify({'error': 'Failed to stream song'}), 500

@app.route('/api/delete/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    try:
        song = Song.query.get_or_404(song_id)
        try:
            os.remove(song.file_path)
        except OSError as e:
            logger.error(f"Error deleting file {song.file_path}: {str(e)}")
        db.session.delete(song)
        db.session.commit()
        return jsonify({'message': 'Song deleted successfully'})
    except Exception as e:
        logger.error(f"Error deleting song {song_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete song'}), 500

@app.route('/api/settings/youtube', methods=['POST'])
def update_youtube_settings():
    try:
        data = request.get_json()
        if not data or 'cookies' not in data:
            return jsonify({'error': 'No cookie data provided'}), 400
            
        # Save cookies to file
        with open(YOUTUBE_COOKIES_FILE, 'w') as f:
            json.dump(data['cookies'], f)
            
        return jsonify({'message': 'YouTube settings updated successfully'})
    except Exception as e:
        logger.error(f"Error updating YouTube settings: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/youtube/download', methods=['POST'])
def download_youtube():
    try:
        data = request.get_json()
        if not data or 'url' not in data:
            return jsonify({'error': 'No URL provided'}), 400
            
        url = data['url']
        logger.info(f"Downloading from YouTube: {url}")
        
        # Load cookies if they exist
        cookies = None
        if os.path.exists(YOUTUBE_COOKIES_FILE):
            try:
                with open(YOUTUBE_COOKIES_FILE, 'r') as f:
                    cookies = json.load(f)
            except Exception as e:
                logger.error(f"Error loading YouTube cookies: {str(e)}")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(UPLOAD_DIR, '%(title)s.%(ext)s'),
            'verbose': True,
            'cookiefile': YOUTUBE_COOKIES_FILE if cookies else None,
            'cookiesfrombrowser': None,  # Disable browser cookies when using file
            'extractor_args': {'youtube': {
                'player_client': ['android', 'web'],
                'player_skip': [],  # Don't skip anything when authenticated
            }},
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'no_warnings': False,
            'quiet': False
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            
            # Create song entry
            song = Song(
                filename=os.path.basename(filename),
                title=info.get('title'),
                artist=info.get('uploader'),
                file_path=filename
            )
            db.session.add(song)
            db.session.commit()
            
            logger.info(f"Successfully downloaded: {filename}")
            return jsonify({
                'message': 'Download successful',
                'filename': os.path.basename(filename)
            })
            
    except Exception as e:
        logger.error(f"YouTube download error: {str(e)}")
        return jsonify({'error': str(e)}), 500

# Create database tables
with app.app_context():
    db.create_all()
    logger.info("Database tables created successfully")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 