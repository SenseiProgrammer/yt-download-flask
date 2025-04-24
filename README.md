# YT Downloader - Flask Backend

This is a complete Flask-based backend for a YouTube video/audio downloader. It uses `yt-dlp` and `ffmpeg` to fetch, convert, and save files with clean filenames and supports video/audio selection, playlist downloads, and automatic format naming.

---

## Features

- Download **YouTube videos or audio** in selected quality
- Supports **video quality selection** (240p to 2160p)
- Automatically names files: `Video Title[YT-Downloader].mp3` / `.mp4`
- Supports full **playlist downloading**
- Saves files to `downloads/` folder
- Displays a list of downloaded files in frontend
- Shows **progress bar** during download
- Uses `ffmpeg` and `ffprobe` for format conversion

---

## Tech Stack

- Python 3
- Flask
- yt-dlp
- ffmpeg & ffprobe

---

## Installation (for Railway or Local)

1. Upload the project to GitHub or Railway
2. Make sure `ffmpeg` and `ffprobe` binaries are in the root folder
3. Add environment variable:

PORT = 5000

4. Build & Start Commands (Railway):

pip install -r requirements.txt python main.py

---

## Folder Structure

. ├── main.py                 # Flask backend ├── index.html              # Frontend UI ├── ffmpeg / ffprobe        # Binaries for media processing ├── downloads/              # Where files are saved └── requirements.txt        # Python dependencies

---

## API Endpoints

- `POST /api/info`  
  Get video title & thumbnail from a YouTube URL

- `POST /api/download`  
  Download video/audio with specified settings

- `GET /downloads`  
  List all downloaded files

---

## Developed by

**Ronak Satish Deshmukh**  
YT Downloader App | Powered by Flask + yt-dlp + ffmpeg

---

## License

MIT License (Free to use with attribution)


---
