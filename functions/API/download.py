from http import HTTPStatus
import json
import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Import utilities
import sys
sys.path.append('./vendor')

from utils.platform_detector import detect_platform
from utils.youtube import extract_youtube_video
from utils.tiktok import extract_tiktok_video
from utils.facebook import extract_facebook_video
from utils.instagram import extract_instagram_video
from utils.twitter import extract_twitter_video
from utils.reddit import extract_reddit_video

# Developer Info
DEVELOPER = {
    "api_name": "SOCIAL DL - Cloudflare Edition",
    "api_version": "1.0.0",
    "api_developer": "DARK FORID",
    "dev_github": "https://github.com/DARK-FORID-404",
    "dev_telegram": "https://t.me/@UnknownXBoyX"
}

def on_request(request):
    """Main entry point for Cloudflare Pages"""
    
    # Parse URL parameters
    url_parts = urlparse(str(request.url))
    params = parse_qs(url_parts.query)
    
    video_url = params.get('url', [None])[0]
    video_format = params.get('format', ['video'])[0]
    quality = params.get('quality', ['best'])[0]
    
    if not video_url:
        return json.dumps({
            "success": False,
            "error": "Missing required param: ?url=",
            "developer": DEVELOPER
        }), HTTPStatus.BAD_REQUEST, {'Content-Type': 'application/json'}
    
    try:
        # Detect platform
        platform = detect_platform(video_url)
        
        if platform == "youtube":
            result = extract_youtube_video(video_url, video_format, quality)
        elif platform == "tiktok":
            result = extract_tiktok_video(video_url)
        elif platform == "facebook":
            result = extract_facebook_video(video_url)
        elif platform == "instagram":
            result = extract_instagram_video(video_url)
        elif platform == "twitter":
            result = extract_twitter_video(video_url)
        elif platform == "reddit":
            result = extract_reddit_video(video_url)
        else:
            return json.dumps({
                "success": False,
                "error": "Unsupported platform. Please use TikTok, Facebook, Instagram, Twitter, Reddit, or YouTube.",
                "developer": DEVELOPER
            }), HTTPStatus.BAD_REQUEST, {'Content-Type': 'application/json'}
        
        if result:
            return json.dumps({
                "success": True,
                "platform": platform,
                "developer": DEVELOPER,
                "result": result
            }), HTTPStatus.OK, {'Content-Type': 'application/json'}
        else:
            return json.dumps({
                "success": False,
                "error": f"Failed to extract {platform} video",
                "developer": DEVELOPER
            }), HTTPStatus.NOT_FOUND, {'Content-Type': 'application/json'}
            
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e),
            "developer": DEVELOPER
        }), HTTPStatus.INTERNAL_SERVER_ERROR, {'Content-Type': 'application/json'}

# For local testing
if __name__ == "__main__":
    import sys
    # Quick test
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    result = on_request(test_url)
    print(result)
