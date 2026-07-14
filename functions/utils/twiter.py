import re
import requests

def extract_twitter_video(url):
    """Extract Twitter/X video information"""
    
    try:
        # Use Twitter API (unofficial)
        api_url = f"https://twittersave.com/api/v1/video?url={url}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "id": extract_twitter_id(url),
                    "title": data.get("title", "Twitter Video"),
                    "uploader": data.get("username", "Twitter User"),
                    "duration_seconds": 0,
                    "thumbnail": data.get("thumbnail", ""),
                    "webpage_url": url,
                    "quality": "HD",
                    "direct_url": data.get("video_url"),
                    "video_urls": [{"quality": "HD", "url": data.get("video_url")}]
                }
    except:
        pass
    
    return None

def extract_twitter_id(url):
    """Extract Twitter/X tweet ID"""
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    return None
