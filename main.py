from flask import Flask, request, jsonify, send_from_directory
from yt_dlp import YoutubeDL
import os
import re

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "downloads")
FFMPEG_PATH = os.path.dirname(__file__)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/api/info", methods=["POST"])
def video_info():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    with YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        return jsonify({
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail")
        })

@app.route("/api/download", methods=["POST"])
def download():
    data = request.json
    url = data.get("url")
    type_ = data.get("type")
    quality = data.get("quality")
    is_playlist = data.get("isPlaylist", False)

    if not url or not type_:
        return jsonify({"error": "Missing fields"}), 400

    try:
        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = re.sub(r'[\\/*?:"<>|]', '', info.get("title"))
            output_template = os.path.join(DOWNLOAD_FOLDER, f"{title}[YT-Downloader].%(ext)s")
    except Exception as e:
        return jsonify({"error": "Failed to fetch video title"}), 500

    ydl_opts = {
        "outtmpl": output_template,
        "ffmpeg_location": FFMPEG_PATH,
        "noplaylist": not is_playlist,
        "progress_hooks": [hook],
    }

    if type_ == "audio":
        ydl_opts["format"] = "bestaudio"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }]
    else:
        ydl_opts["format"] = f"bestvideo[height<={quality}]+bestaudio"
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }]

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"message": "Download completed."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/downloads")
def list_downloads():
    files = [f for f in os.listdir(DOWNLOAD_FOLDER) if os.path.isfile(os.path.join(DOWNLOAD_FOLDER, f))]
    return jsonify(files)

def hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d['_percent_str']} - {d['_eta_str']} remaining")

if __name__ == "__main__":
    app.run(debug=True)
