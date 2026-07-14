import re

PLATFORMS = {
    "youtube": r"(youtube\.com|youtu\.be)",
    "tiktok": r"tiktok\.com",
    "facebook": r"(facebook\.com|fb\.watch)",
    "instagram": r"instagram\.com",
    "twitter": r"(twitter\.com|x\.com)",
    "reddit": r"reddit\.com",
    "vimeo": r"vimeo\.com",
    "dailymotion": r"dailymotion\.com",
    "soundcloud": r"soundcloud\.com",
    "twitch": r"twitch\.tv",
}

def detect_platform(url):
    """Detect platform from URL"""
    for platform, pattern in PLATFORMS.items():
        if re.search(pattern, url, re.IGNORECASE):
            return platform
    return "unknown"

def extract_video_id(url, platform):
    """Extract video ID based on platform"""
    if platform == "youtube":
        # YouTube ID extraction
        import re
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11})',
            r'youtu\.be\/([0-9A-Za-z_-]{11})',
            r'embed\/([0-9A-Za-z_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
    
    elif platform == "tiktok":
        # TikTok ID extraction
        import re
        match = re.search(r'/video/(\d+)', url)
        if match:
            return match.group(1)
    
    elif platform == "facebook":
        # Facebook ID extraction
        import re
        match = re.search(r'/videos/(\d+)', url)
        if match:
            return match.group(1)
    
    return None
