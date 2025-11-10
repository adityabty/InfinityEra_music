import aiohttp, os
from pathlib import Path

Api_key = os.getenv("Api_key")
Api_url = os.getenv("Api_url", "").rstrip("/")

async def fetch_song(query: str):
    """Fetch a song from your YT API endpoint"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{Api_url}/search", params={"query": query, "key": Api_key}) as r:
                data = await r.json()
                if data.get("status") != "ok":
                    return None, None
                info = data["results"][0]
                return info["url"], info["title"]
    except Exception as e:
        print("fetch_song error:", e)
        return None, None

async def download_song(url: str, title: str):
    """Download song audio from YT API URL"""
    file_path = Path(f"downloads/{title}.mp3")
    file_path.parent.mkdir(exist_ok=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            with open(file_path, "wb") as f:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
    return str(file_path)
