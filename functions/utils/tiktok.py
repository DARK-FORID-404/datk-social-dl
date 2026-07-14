import re
import json
import requests

def extract_tiktok_video(url):
    """Extract TikTok video information"""
    
    # Try to get video ID
    video_id = extract_tiktok_id(url)
    if not video_id:
        return None
    
    try:
        # Use TikTok API endpoint (unofficial)
        api_url = f"https://www.tikwm.com/api/?url={url}&hd=1"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 0:
                video_data = data.get("data", {})
                
                return {
                    "id": video_id,
                    "title": video_data.get("title", "TikTok Video"),
                    "uploader": video_data.get("author", {}).get("unique_id", "Unknown"),
                    "duration_seconds": video_data.get("duration", 0),
                    "view_count": video_data.get("play_count", 0),
                    "like_count": video_data.get("digg_count", 0),
                    "thumbnail": video_data.get("cover", ""),
                    "webpage_url": url,
                    "quality": "HD",
                    "direct_url": video_data.get("play", ""),
                    "video_urls": [{
                        "quality": "HD",
                        "url": video_data.get("play", "")
                    }]
                }
    except:
        pass
    
    # Fallback to another API
    try:
        api_url = f"https://tikmate.cc/api/v1/video?url={url}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "id": video_id,
                    "title": data.get("title", "TikTok Video"),
                    "uploader": "TikTok User",
                    "duration_seconds": 0,
                    "thumbnail": data.get("thumbnail", ""),
                    "webpage_url": url,
                    "quality": "HD",
                    "direct_url": data.get("video_url", "")
                }
    except:
        pass
    
    return None

def extract_tiktok_id(url):
    """Extract TikTok video ID"""
    # Try different patterns
    patterns = [
        r'/video/(\d+)',
        r'v/(\d+)',
        r'tiktok\.com/@[^/]+/video/(\d+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
