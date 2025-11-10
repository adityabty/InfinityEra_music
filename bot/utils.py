# utils.py

import re
import datetime

# Regular expression to clean up common unwanted text from song titles
CLEAN_TITLE_REGEX = re.compile(
    r"(\s*\[[^\]]+\]|\s*\([^\)]+\)|\s*[-—–]\s*Official\s*Video)",
    re.IGNORECASE
)

def format_duration(seconds: int) -> str:
    """
    Formats the duration in seconds into H:MM:SS or MM:SS format.
    Example: 3661 -> 1:01:01
             185  -> 3:05
    """
    if seconds is None:
        return "N/A"
        
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "N/A"

    if seconds < 0:
        return "0:00"

    # Use datetime.timedelta for easy formatting
    timedelta = datetime.timedelta(seconds=seconds)
    
    # Calculate hours, minutes, seconds
    total_minutes = seconds // 60
    hours = total_minutes // 60
    minutes = total_minutes % 60
    remaining_seconds = seconds % 60

    if hours > 0:
        # Format as H:MM:SS
        return f"{hours}:{minutes:02}:{remaining_seconds:02}"
    else:
        # Format as MM:SS
        return f"{minutes}:{remaining_seconds:02}"


def clean_title(title: str) -> str:
    """
    Removes common garbage data (e.g., [Official Video], (Lyrics)) from YouTube titles.
    """
    if not isinstance(title, str):
        return title
        
    cleaned = CLEAN_TITLE_REGEX.sub('', title).strip()
    return cleaned
    
# --- Example of another utility function ---

def get_readable_bytes(size: int) -> str:
    """
    Converts file size (in bytes) to a human-readable format (KB, MB, GB).
    """
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    if size == 0:
        return "0 Byte"
    
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024
        i += 1
    
    return f"{size:.2f} {units[i]}"

