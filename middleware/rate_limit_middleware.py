"""
Rate Limiting Middleware

Implements intelligent rate limiting with:
- IP-based limiting
- Agent-specific quotas (higher for known AI agents)
- Redis-backed tracking
- Rate limit event logging
"""

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config.site_config import SiteConfig
from services.monitoring_service import monitoring
import re


def get_identifier():
    """
    Get identifier for rate limiting.
    
    Uses IP address as primary identifier, but also considers:
    - X-Forwarded-For header (for proxied requests)
    - User-Agent (for agent-specific limits)
    
    Returns:
        str: Identifier for rate limiting
    """
    # Check for forwarded IP (behind proxy/load balancer)
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        # Get first IP in chain (original client)
        ip = forwarded_for.split(',')[0].strip()
    else:
        ip = get_remote_address()
    
    return ip


def is_ai_agent(user_agent: str) -> tuple[bool, str]:
    """
    Detect if the request is from a known AI agent.
    
    Args:
        user_agent: User-Agent header value
        
    Returns:
        tuple: (is_agent, agent_name)
    """
    if not user_agent:
        return False, None
    
    # Known AI agent patterns
    ai_agents = {
        'GPTBot': r'GPTBot',
        'Claude-Web': r'Claude-Web|anthropic-ai',
        'PerplexityBot': r'PerplexityBot',
        'Googlebot-AI': r'Google-Extended|Googlebot-AI',
        'Meta-AI': r'Meta-AI|FacebookBot',
        'AppleBot-AI': r'Applebot-Extended',
        'Bingbot': r'bingbot',
        'Slackbot': r'Slackbot',
        'Twitterbot': r'Twitterbot'
    }
    
    user_agent_lower = user_agent.lower()
    
    for agent_name, pattern in ai_agents.items():
        if re.search(pattern, user_agent, re.IGNORECASE):
            return True, agent_name
    
    return False, None


def get_rate_limit():
    """
    Get rate limit for current request.
    
    Returns higher limits for known AI agents.
    
    Returns:
        str: Rate limit string (e.g., "100 per minute")
    """
    user_agent = request.headers.get('User-Agent', '')
    is_agent, agent_name = is_ai_agent(user_agent)
    
    if is_agent and agent_name:
        # Get agent-specific rate limit
        limit = SiteConfig.get_rate_limit_for_agent(agent_name)
        return f"{limit} per minute"
    
    # Default rate limit
    return f"{SiteConfig.RATE_LIMIT_PER_MINUTE} per minute"


def rate_limit_exceeded_handler(e):
    """
    Custom handler for rate limit exceeded errors.
    
    Logs the event and returns a JSON response.
    
    Args:
        e: RateLimitExceeded exception
        
    Returns:
        tuple: (JSON response, HTTP status code)
    """
    # Extract rate limit info
    user_agent = request.headers.get('User-Agent', '')
    ip = get_identifier()
    is_agent, agent_name = is_ai_agent(user_agent)
    
    # Log rate limit event
    monitoring.log_rate_limit_event(
        ip_address=ip,
        user_agent=user_agent,
        endpoint=request.endpoint or request.path,
        limit_type='per_minute',
        agent_name=agent_name if is_agent else None
    )
    
    # Calculate retry_after from rate limit window
    retry_after = 60  # Default to 60 seconds
    
    response = jsonify({
        "success": False,
        "error": "Rate limit exceeded",
        "message": "Too many requests. Please slow down.",
        "retry_after": retry_after,
        "limit": get_rate_limit(),
        "documentation": f"{SiteConfig.SITE_URL}/api/docs#rate-limits"
    })
    
    # Add rate limit headers
    response.headers['Retry-After'] = str(retry_after)
    response.headers['X-RateLimit-Limit'] = str(SiteConfig.RATE_LIMIT_PER_MINUTE)
    response.headers['X-RateLimit-Remaining'] = '0'
    
    return response, 429


def init_rate_limiting(app: Flask):
    """
    Initialize rate limiting for the Flask application.
    
    Args:
        app: Flask application instance
    """
    if not SiteConfig.RATE_LIMIT_ENABLED:
        print("⚠ Rate limiting is disabled")
        return
    
    # Initialize limiter with Redis storage
    limiter = Limiter(
        app=app,
        key_func=get_identifier,
        default_limits=[
            f"{SiteConfig.RATE_LIMIT_PER_MINUTE} per minute",
            f"{SiteConfig.RATE_LIMIT_PER_HOUR} per hour"
        ],
        storage_uri=SiteConfig.REDIS_URL,
        strategy="fixed-window",
        on_breach=rate_limit_exceeded_handler
    )
    
    # Apply dynamic rate limits to API endpoints
    @limiter.request_filter
    def exempt_health_check():
        """Exempt health check endpoint from rate limiting."""
        return request.endpoint == 'health'
    
    # Add rate limit headers to all responses
    @app.after_request
    def add_rate_limit_headers(response):
        """Add rate limit information to response headers."""
        if not SiteConfig.RATE_LIMIT_ENABLED:
            return response
        
        # Skip for non-API endpoints
        if not request.path.startswith('/api'):
            return response
        
        # Get rate limit for this request
        user_agent = request.headers.get('User-Agent', '')
        is_agent, agent_name = is_ai_agent(user_agent)
        
        if is_agent and agent_name:
            limit = SiteConfig.get_rate_limit_for_agent(agent_name)
        else:
            limit = SiteConfig.RATE_LIMIT_PER_MINUTE
        
        response.headers['X-RateLimit-Limit'] = str(limit)
        
        # Note: Flask-Limiter will add X-RateLimit-Remaining and X-RateLimit-Reset
        
        return response
    
    # Apply custom rate limits to specific endpoints
    
    # Higher limits for batch processing (more expensive operation)
    @limiter.limit("50 per minute")
    def batch_limit():
        return request.endpoint == 'batch.batch_process'
    
    # Lower limits for operations listing (informational endpoint)
    @limiter.limit("200 per minute")
    def operations_limit():
        return request.endpoint == 'batch.list_operations'
    
    print(f"✓ Rate limiting initialized")
    print(f"  Default limit: {SiteConfig.RATE_LIMIT_PER_MINUTE} requests/minute")
    print(f"  AI agent limit: 200 requests/minute")
    print(f"  Storage: Redis ({SiteConfig.REDIS_URL})")
    print(f"  Strategy: Fixed window")
    
    return limiter


def get_rate_limit_status(ip_address: str) -> dict:
    """
    Get current rate limit status for an IP address.
    
    Args:
        ip_address: IP address to check
        
    Returns:
        dict: Rate limit status information
    """
    # This would query Redis for current usage
    # For now, return placeholder data
    return {
        "ip_address": ip_address,
        "requests_made": 0,
        "limit": SiteConfig.RATE_LIMIT_PER_MINUTE,
        "remaining": SiteConfig.RATE_LIMIT_PER_MINUTE,
        "reset_at": None
    }
