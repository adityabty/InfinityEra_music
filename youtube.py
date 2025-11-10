import yt_dlp
import os

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'geo_bypass': True,
    'nocheckcertificate': True,
    'extract_flat': 'in_playlist',
    'quiet': True,
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

async def get_youtube_info(query: str):
    """
    Fetches required information (URL, title, thumbnail) from YouTube using a query or URL.
    Returns: {title, stream_url, thumbnail_url, duration}
    """
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            # Check if it's a direct URL
            if 'https://' in query:
                info = ydl.extract_info(query, download=False)
            else:
                # Search query
                info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
        except Exception as e:
            print(f"YouTube Fetching Error: {e}")
            return None

        # The 'url' in the final format should be the direct audio stream URL
        stream_url = info.get('url') # This might require further processing depending on the format chosen
        
        return {
            "title": info.get('title'),
            "stream_url": stream_url,
            "thumbnail_url": info.get('thumbnail'),
            "duration": info.get('duration')
        }

# NOTE: PyTgCalls streaming requires a direct accessible audio URL or a local file path.
# yt-dlp often provides a direct URL that can be passed to PyTgCalls' InputStream.
