import re
import requests

def extract_instagram_video(url):
    """Extract Instagram video/reel information"""
    
    try:
        # Use instagram API (unofficial)
        api_url = f"https://instagram.com/api/v1/media?url={url}"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                video_urls = data.get("video_urls", [])
                if video_urls:
                    return {
                        "id": extract_instagram_id(url),
                        "title": data.get("title", "Instagram Video"),
                        "uploader": data.get("username", "Instagram User"),
                        "duration_seconds": 0,
                        "thumbnail": data.get("thumbnail", ""),
                        "webpage_url": url,
                        "quality": "HD",
                        "direct_url": video_urls[0],
                        "video_urls": [{"quality": "HD", "url": v} for v in video_urls]
                    }
    except:
        pass
    
    return None

def extract_instagram_id(url):
    """Extract Instagram post/reel ID"""
    match = re.search(r'/p/([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    match = re.search(r'/reel/([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    return None
