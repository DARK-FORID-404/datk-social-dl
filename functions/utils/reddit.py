import re
import requests

def extract_reddit_video(url):
    """Extract Reddit video information"""
    
    try:
        # Use Reddit API
        # Convert to JSON endpoint
        if "reddit.com/r/" in url:
            # Add .json to get API data
            if not url.endswith(".json"):
                url = url + ".json"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                post_data = data[0].get("data", {}).get("children", [{}])[0].get("data", {})
                video_url = post_data.get("media", {}).get("reddit_video", {}).get("fallback_url")
                if video_url:
                    return {
                        "id": post_data.get("id", ""),
                        "title": post_data.get("title", "Reddit Video"),
                        "uploader": post_data.get("author", "Reddit User"),
                        "duration_seconds": 0,
                        "thumbnail": post_data.get("thumbnail", ""),
                        "webpage_url": url,
                        "quality": "HD",
                        "direct_url": video_url,
                        "video_urls": [{"quality": "HD", "url": video_url}]
                    }
    except:
        pass
    
    return None
