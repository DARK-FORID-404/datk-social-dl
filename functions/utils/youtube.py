import re
import json
import requests
from datetime import datetime

def extract_youtube_video(url, format_type="video", quality="best"):
    """Extract YouTube video information"""
    
    # Extract video ID
    video_id = extract_youtube_id(url)
    if not video_id:
        return None
    
    # Fetch video page
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.5"
    }
    
    try:
        response = requests.get(f"https://www.youtube.com/watch?v={video_id}", headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        
        html = response.text
        
        # Extract initial player response
        match = re.search(r'ytInitialPlayerResponse\s*=\s*({.*?});', html, re.DOTALL)
        if not match:
            return None
        
        player_data = json.loads(match.group(1))
        video_details = player_data.get("videoDetails", {})
        streaming_data = player_data.get("streamingData", {})
        
        # Extract video info
        title = video_details.get("title", "Untitled")
        uploader = video_details.get("author", "Unknown")
        duration = int(video_details.get("lengthSeconds", 0))
        
        # Get thumbnail
        thumbnail = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        
        # Extract video formats
        formats = streaming_data.get("formats", [])
        adaptive_formats = streaming_data.get("adaptiveFormats", [])
        
        # Build response
        result = {
            "id": video_id,
            "title": title,
            "uploader": uploader,
            "duration_seconds": duration,
            "view_count": int(video_details.get("viewCount", 0)),
            "thumbnail": thumbnail,
            "webpage_url": f"https://www.youtube.com/watch?v={video_id}",
            "quality": quality,
            "format": format_type,
            "video_urls": [],
            "audio_urls": []
        }
        
        # Extract video URLs (with quality options)
        for fmt in formats:
            if "url" in fmt:
                height = fmt.get("height", 0)
                width = fmt.get("width", 0)
                if height > 0:
                    result["video_urls"].append({
                        "quality": f"{height}p",
                        "height": height,
                        "width": width,
                        "fps": fmt.get("fps", 30),
                        "url": fmt["url"],
                        "filesize": int(fmt.get("contentLength", 0) or 0)
                    })
        
        # Sort by quality
        result["video_urls"].sort(key=lambda x: x["height"], reverse=True)
        
        # Extract audio URLs
        for fmt in adaptive_formats:
            if "audio" in fmt.get("mimeType", "") and "url" in fmt:
                result["audio_urls"].append({
                    "bitrate": fmt.get("bitrate", 0),
                    "url": fmt["url"],
                    "filesize": int(fmt.get("contentLength", 0) or 0)
                })
        
        # Filter by requested quality
        if quality.isdigit():
            target_height = int(quality)
            result["video_urls"] = [v for v in result["video_urls"] if v["height"] <= target_height]
        
        # Get best video and audio URLs
        if format_type == "audio":
            if result["audio_urls"]:
                result["direct_url"] = result["audio_urls"][0]["url"]
            else:
                # Fallback to video with audio
                if result["video_urls"]:
                    result["direct_url"] = result["video_urls"][0]["url"]
        else:
            if result["video_urls"]:
                result["direct_url"] = result["video_urls"][0]["url"]
            elif result["audio_urls"]:
                result["direct_url"] = result["audio_urls"][0]["url"]
        
        return result
        
    except Exception as e:
        print(f"Error extracting YouTube: {e}")
        return None

def extract_youtube_id(url):
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11})',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'embed\/([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
