# 🎬 YouTube Downloader

A simple and elegant Streamlit web app for downloading YouTube videos and playlists.

## Features

- 🎥 **Video Download**: Download individual YouTube videos
- 📚 **Playlist Download**: Download entire playlists at once
- 🎛️ **Quality Selection**: Choose from various quality options (Best, 1080p, 720p, 480p, 360p, Audio only)
- 📁 **File Management**: View downloaded files and open the downloads folder
- 🎨 **User-Friendly UI**: Built with Streamlit for an intuitive interface

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or navigate to the project directory**:
```bash
cd "Youtube Downloader"
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Streamlit app**:
```bash
streamlit run app.py
```

2. **Open your browser** (it should open automatically):
```
http://localhost:8501
```

3. **Use the app**:
   - Select **Video** or **Playlist** from the sidebar toggle
   - Paste your YouTube URL in the text input
   - Choose your desired video quality
   - Click the **Download** button
   - Monitor the download progress

## Supported Quality Options

### Video Downloads
- **Best (MP4)**: Highest quality MP4 format
- **1080p**: Full HD quality
- **720p**: HD quality
- **480p**: Standard quality
- **360p**: Lower quality (faster download)
- **Audio only (MP3)**: Extract audio as MP3

### Playlist Downloads
- **Best (MP4)**: Highest quality MP4 format
- **720p**: HD quality
- **480p**: Standard quality
- **Audio only (MP3)**: Extract audio as MP3

## Output

All downloaded files are saved to the `downloads/` folder in the project directory. Playlists are organized in subfolders by playlist title.

## Troubleshooting

### "yt-dlp is not installed" error
Make sure you've installed the requirements:
```bash
pip install -r requirements.txt
```

### Download fails
- Verify the YouTube URL is correct and valid
- Check your internet connection
- Try a lower quality setting if bandwidth is limited

### FFmpeg missing (for format conversion)
If you need to convert between formats, install FFmpeg:

**macOS**:
```bash
brew install ffmpeg
```

**Ubuntu/Debian**:
```bash
sudo apt-get install ffmpeg
```

**Windows**:
```bash
choco install ffmpeg
```

## Disclaimer

This tool is for personal use only. Always respect YouTube's Terms of Service and content creators' rights. Only download content you have permission to download.

## License

MIT License
