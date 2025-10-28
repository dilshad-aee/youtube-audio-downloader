# YouTube Audio Downloader

[![Build Android APK](https://github.com/dilshad-aee/youtube-audio-downloader/actions/workflows/build.yml/badge.svg)](https://github.com/dilshad-aee/youtube-audio-downloader/actions/workflows/build.yml)

A modern cross-platform application built with Python and Kivy for downloading audio from YouTube videos using yt-dlp.

**Available for:** Desktop (Windows, Mac, Linux) and Android

## Features

- 🎵 Download audio from YouTube videos in MP3 format (192kbps)
- 📊 Real-time download progress tracking
- 📁 Custom download location selection
- 🎨 Modern, user-friendly GUI
- ⚡ Fast and efficient downloads
- 🔄 Threading support for non-blocking UI

## Prerequisites

- Python 3.8 or higher
- FFmpeg (required for audio conversion)

### Installing FFmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Installation

### 📱 Android

**Download the latest APK:**
1. Go to [Actions](https://github.com/dilshad-aee/youtube-audio-downloader/actions)
2. Click on the latest successful build
3. Download the APK from "Artifacts"
4. Install on your Android device

Or build it yourself - see [UPLOAD_TO_GITHUB.md](UPLOAD_TO_GITHUB.md)

### 🖥️ Desktop

1. **Clone or download this project**

2. **Create a virtual environment (recommended):**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

## Usage

1. **Run the application:**
```bash
python main.py
```

2. **Download audio:**
   - Paste a YouTube video URL in the input field
   - Choose a download location (default: Downloads folder)
   - Click "Download Audio"
   - Wait for the download to complete

## Features Explained

### User Interface
- **YouTube URL Input**: Enter the URL of the YouTube video
- **Save Location**: Choose where to save the downloaded audio file
- **Progress Bar**: Visual feedback showing download progress
- **Status Display**: Detailed information about the download process

### Download Process
1. Fetches video information
2. Downloads the best available audio quality
3. Converts to MP3 format (192kbps)
4. Saves with the original video title as filename

## Troubleshooting

### "No module named 'kivy'"
Make sure you've installed the requirements:
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
Install FFmpeg using the instructions in the Prerequisites section.

### Download fails
- Check your internet connection
- Verify the YouTube URL is correct and accessible
- Some videos may be restricted or unavailable in your region

### Permission errors
Make sure you have write permissions for the selected download folder.

## Technical Details

- **Framework**: Kivy 2.3.0
- **Downloader**: yt-dlp 2024.8.6
- **Audio Format**: MP3 (192kbps)
- **Threading**: Uses Python threading for non-blocking downloads

## Project Structure

```
SP-WIN/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Dependencies

- `kivy==2.3.0` - Cross-platform GUI framework
- `yt-dlp==2024.8.6` - YouTube video/audio downloader

## License

This project is for educational purposes. Please respect YouTube's Terms of Service and copyright laws when downloading content.

## Notes

- Downloaded files are saved with the video title as the filename
- The app requires an active internet connection
- Large files may take longer to download depending on your connection speed
- Progress percentage, download speed, and ETA are displayed in real-time

## Support

If you encounter any issues:
1. Make sure FFmpeg is installed and accessible
2. Check that you have the latest version of Python
3. Verify all dependencies are installed correctly
4. Ensure you have write permissions for the download folder

---

**Enjoy downloading your favorite YouTube audio!** 🎵
