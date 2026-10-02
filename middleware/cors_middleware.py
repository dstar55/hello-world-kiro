"""
CORS Middleware for Cross-Origin Requests

Enables AI agents and web applications to access the API from different origins.
Configured to be secure yet flexible for legitimate use cases.
"""

from flask import Flask, request
from config.site_config import SiteConfig


def init_cors_middleware(app: Flask):
    """
    Initialize CORS middleware for the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.after_request
    def add_cors_headers(response):
        """
        Add CORS headers to all responses.
        
        Security considerations:
        - Allows all origins for public API
        - Allows common HTTP methods
        - Allows standard headers plus custom ones
        - Caches preflight for 1 hour
        """
        
        # Get origin from request
        origin = request.headers.get('Origin', '*')
        
        # Allow the requesting origin (for credentials support in future)
        response.headers['Access-Control-Allow-Origin'] = origin
        
        # Allow credentials (for future authentication)
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        
        # Allow common HTTP methods
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        
        # Allow common headers plus custom ones
        allowed_headers = [
            'Content-Type',
            'Authorization',
            'X-Requested-With',
            'X-API-Key',
            'X-Agent-Name',
            'X-Agent-Version',
            'Accept',
            'Origin'
        ]
        response.headers['Access-Control-Allow-Headers'] = ', '.join(allowed_headers)
        
        # Expose custom headers to client
        exposed_headers = [
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining',
            'X-RateLimit-Reset',
            'X-Request-ID',
            'X-Response-Time'
        ]
        response.headers['Access-Control-Expose-Headers'] = ', '.join(exposed_headers)
        
        # Cache preflight requests for 1 hour
        response.headers['Access-Control-Max-Age'] = '3600'
        
        return response
    
    @app.before_request
    def handle_preflight():
        """
        Handle OPTIONS preflight requests.
        """
        if request.method == 'OPTIONS':
            response = app.make_default_options_response()
            return response
    
    print(f"✓ CORS middleware initialized")
    print(f"  Allowed origins: All (public API)")
    print(f"  Allowed methods: GET, POST, PUT, DELETE, OPTIONS, PATCH")
    print(f"  Preflight cache: 1 hour")
