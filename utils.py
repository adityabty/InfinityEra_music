# utils.py
import os
import subprocess
import shlex
from youtubesearchpython import VideosSearch
from config import DOWNLOADS_DIR, LOG_CHANNEL
from PIL import Image, ImageFont, ImageDraw

def yt_search(query):
    """Return top result dict: title, link, duration, thumbnail"""
    vs = VideosSearch(query, limit=1)
    res = vs.result()
    if res and res.get("result"):
        item = res["result"][0]
        return {
            "title": item.get("title"),
            "link": item.get("link"),
            "duration": item.get("duration"),
            "thumbnail": item.get("thumbnails", [{}])[-1].get("url")
        }
    return None

def download_audio(url, filename=None):
    """
    Use yt-dlp to download best audio as .mp3 into DOWNLOADS_DIR.
    Returns path to file.
    """
    if filename is None:
        filename = "%(title)s.%(ext)s"
    out_template = os.path.join(DOWNLOADS_DIR, filename)
    cmd = f'yt-dlp -x --audio-format mp3 -o "{out_template}" "{url}" --no-playlist'
    process = subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # find generated file
    # naive way: list DOWNLOADS_DIR sorted by mtime
    files = sorted([os.path.join(DOWNLOADS_DIR, f) for f in os.listdir(DOWNLOADS_DIR)], key=os.path.getmtime, reverse=True)
    for f in files:
        if f.lower().endswith(".mp3") or f.lower().endswith(".m4a") or f.lower().endswith(".opus"):
            return f
    return None

def create_nowplaying_image(thumbnail_path_or_url, title, requester_mention, output_path):
    """
    Load thumbnail (local path or URL), overlay InfinityEra logo bottom-right and put caption text below.
    Saves to output_path.
    """
    # open thumbnail (if URL, download temporarily)
    from io import BytesIO
    import requests

    if thumbnail_path_or_url.startswith("http"):
        r = requests.get(thumbnail_path_or_url, timeout=15)
        img = Image.open(BytesIO(r.content)).convert("RGBA")
    else:
        img = Image.open(thumbnail_path_or_url).convert("RGBA")

    # Resize to width 1280 preserving aspect
    base_w = 1280
    wpercent = (base_w / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_w, hsize), Image.LANCZOS)

    # paste logo bottom-right (assets/infinity_logo.png)
    logo_path = os.path.join("assets", "infinity_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_w = int(base_w * 0.18)
        logo.thumbnail((logo_w, logo_w), Image.ANTIALIAS)
        img.paste(logo, (img.width - logo.width - 20, img.height - logo.height - 20), logo)

    # create final canvas adding caption area
    caption_h = 200
    canvas = Image.new("RGBA", (img.width, img.height + caption_h), (20,20,20,255))
    canvas.paste(img, (0,0))

    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except:
        font = ImageFont.load_default()

    text_x = 30
    text_y = img.height + 20
    draw.text((text_x, text_y), f"🎧 Now Playing: {title}", font=font, fill=(255,255,255,255))
    draw.text((text_x, text_y+40), f"🎤 Requested by: {requester_mention}", font=font, fill=(200,200,200,255))
    draw.text((text_x, text_y+80), f"✨ Powered by InfinityEra", font=font, fill=(180,180,180,255))

    canvas.convert("RGB").save(output_path, "JPEG", quality=85)
    return output_path
