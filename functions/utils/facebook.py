import re
import requests
import json

def extract_facebook_video(url):
    """Extract Facebook video information"""
    
    try:
        # Use fbdown.net API
        api_url = f"https://fbdown.net/api/v1/video?url={url}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                video_url = data.get("video_url")
                if not video_url.startswith("http"):
                    video_url = "https://fbdown.net" + video_url
                
                return {
                    "id": extract_facebook_id(url),
                    "title": data.get("title", "Facebook Video"),
                    "uploader": "Facebook User",
                    "duration_seconds": 0,
                    "thumbnail": data.get("thumbnail", ""),
                    "webpage_url": url,
                    "quality": "HD",
                    "direct_url": video_url,
                    "video_urls": [{
                        "quality": "HD",
                        "url": video_url
                    }]
                }
    except:
        pass
    
    # Try alternative API
    try:
        api_url = f"https://getvid.cc/api/v1/video?url={url}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {
                    "id": extract_facebook_id(url),
                    "title": data.get("title", "Facebook Video"),
                    "uploader": "Facebook User",
                    "duration_seconds": 0,
                    "thumbnail": data.get("thumbnail", ""),
                    "webpage_url": url,
                    "quality": "HD",
                    "direct_url": data.get("video_url")
                }
    except:
        pass
    
    return None

def extract_facebook_id(url):
    """Extract Facebook video ID"""
    match = re.search(r'/videos/(\d+)', url)
    if match:
        return match.group(1)
    match = re.search(r'fb\.watch/([a-zA-Z0-9]+)', url)
    if match:
        return match.group(1)
    return None
