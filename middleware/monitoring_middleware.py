"""
Flask middleware for automatic request monitoring

Tracks all incoming requests and logs them to monitoring service.
"""

import time
import traceback
from flask import request, g
from services.monitoring_service import monitoring
from config import SiteConfig


def before_request():
    """Start request timer"""
    g.start_time = time.time()


def after_request(response):
    """Log request details after processing"""
    if not SiteConfig.MONITORING_ENABLED:
        return response
    
    try:
        # Calculate response time
        response_time_ms = int((time.time() - g.start_time) * 1000)
        
        # Detect agent type
        user_agent = request.headers.get('User-Agent', '')
        agent_name, agent_type = monitoring.detect_agent(user_agent)
        
        # Build request data
        request_data = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'method': request.method,
            'endpoint': request.endpoint or 'unknown',
            'path': request.path,
            'ip': request.remote_addr or 'unknown',
            'user_agent': user_agent,
            'agent_type': agent_type,
            'agent_name': agent_name,
            'status_code': response.status_code,
            'response_time_ms': response_time_ms,
            'response_size': len(response.get_data())
        }
        
        # Add request body for API calls (excluding large payloads)
        if request.is_json and request.content_length and request.content_length < 10000:
            request_data['request'] = request.get_json(silent=True)
        
        # Add error info if applicable
        if response.status_code >= 400:
            request_data['error_message'] = f"HTTP {response.status_code}"
            if response.is_json:
                try:
                    error_body = response.get_json()
                    if 'error' in error_body:
                        request_data['error_message'] = error_body['error']
                except:
                    pass
        
        # Log the request (async to avoid blocking)
        monitoring.log_request(request_data)
    
    except Exception as e:
        # Never let monitoring break the app
        print(f"Monitoring middleware error: {e}")
    
    return response


def init_monitoring_middleware(app):
    """Register monitoring middleware with Flask app"""
    app.before_request(before_request)
    app.after_request(after_request)
    
    # Add error handler for logging exceptions
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Log unhandled exceptions"""
        try:
            monitoring.log_error({
                'error_type': type(e).__name__,
                'error_message': str(e),
                'stack_trace': traceback.format_exc(),
                'endpoint': request.endpoint or 'unknown',
                'request_data': request.get_json(silent=True) or {},
                'ip_address': request.remote_addr,
                'user_agent': request.headers.get('User-Agent', '')
            })
        except:
            pass
        
        # Re-raise the exception so Flask handles it normally
        raise e
