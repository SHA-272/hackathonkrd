import yt_dlp
import cv2

params = {
    "format": "best[height<=480]",
    "noplaylist": True,
    "quiet": True,
    "dump_single_json": True,
}


def get_video_stream(url: str) -> str:
    with yt_dlp.YoutubeDL(params) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            video_url = info["url"]
            return video_url
        except Exception as e:
            print(f"Error extracting video URL: {e}")
            return None
