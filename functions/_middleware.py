from http import HTTPStatus
import json

async def on_request(request, next_middleware):
    # Add CORS headers
    response = await next_middleware(request)
    
    # Add CORS headers to response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    
    return response
