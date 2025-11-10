from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os

BRANDING_TEXT = "∞ InfinityEra"
FONT_PATH = "path/to/your/font.ttf" # Ensure you have a path to a TTF font file

async def generate_now_playing_image(thumbnail_url: str) -> str:
    """
    Downloads a thumbnail, adds InfinityEra branding, and saves it locally.
    Returns the path to the temporary branded image file.
    """
    try:
        # 1. Download Thumbnail
        response = requests.get(thumbnail_url)
        thumb_img = Image.open(BytesIO(response.content)).convert("RGBA")
        
        width, height = thumb_img.size

        # 2. Prepare Drawing Context
        draw = ImageDraw.Draw(thumb_img)
        
        # Load Font (Adjust size based on image resolution)
        try:
            font = ImageFont.truetype(FONT_PATH, size=int(height / 20))
        except IOError:
            # Fallback to default font if custom font is not found
            font = ImageFont.load_default()

        # 3. Add Branding Text (Bottom Right Corner)
        
        # Calculate text size and position
        text_bbox = draw.textbbox((0, 0), BRANDING_TEXT, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        margin = int(width * 0.03) # 3% margin
        
        position = (width - text_width - margin, height - text_height - margin)
        
        # Add a subtle background/shadow for better visibility (optional)
        draw.text(
            (position[0] - 1, position[1] - 1), 
            BRANDING_TEXT, 
            font=font, 
            fill=(0, 0, 0, 200) # Dark shadow/outline
        )
        
        # Main text
        draw.text(
            position, 
            BRANDING_TEXT, 
            font=font, 
            fill=(255, 255, 255) # White color
        )

        # 4. Save Image
        temp_path = f"downloads/branded_thumb_{os.getpid()}.jpg"
        os.makedirs("downloads", exist_ok=True)
        thumb_img.save(temp_path, "JPEG")
        
        return temp_path
        
    except Exception as e:
        print(f"Image Generation Error: {e}")
        return None
