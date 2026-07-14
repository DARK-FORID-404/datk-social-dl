from http import HTTPStatus
import json

DEVELOPER = {
    "api_name": "SOCIAL DL - Cloudflare Edition",
    "api_version": "1.0.0",
    "api_developer": "DARK FORID",
    "dev_github": "https://github.com/DARK-FORID-404",
    "dev_telegram": "https://t.me/@UnknownXBoyX"
}

def on_request(request):
    return json.dumps({
        "success": True,
        "message": "DARK-DL API is running on Cloudflare Pages",
        "developer": DEVELOPER,
        "endpoints": {
            "/api/download": "Download video/audio",
            "/api/info": "API information",
            "/": "Home page"
        },
        "usage": {
            "download": "/api/download?url=VIDEO_URL&format=video&quality=best"
        }
    }), HTTPStatus.OK, {'Content-Type': 'application/json'}
