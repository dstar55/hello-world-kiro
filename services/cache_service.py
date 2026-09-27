"""
Redis Cache Service

Provides caching functionality with Redis backend.
Includes decorator for easy function result caching.
"""

import redis
import json
import hashlib
from functools import wraps
import os


class CacheService:
    """Redis-based cache service with automatic fallback"""
    
    def __init__(self):
        """Initialize Redis connection"""
        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.redis_client = None
        self.enabled = False
        
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            print(f"✓ Redis connected: {redis_url}")
        except Exception as e:
            print(f"⚠ Redis connection failed: {e}")
            print("  Cache will be disabled, API will work without caching")
        
        self.default_ttl = 3600  # 1 hour default
    
    def get(self, key):
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/error
        """
        if not self.enabled:
            return None
        
        try:
            value = self.redis_client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Cache get error for key '{key}': {e}")
            return None
    
    def set(self, key, value, ttl=None):
        """
        Set value in cache with TTL
        
        Args:
            key: Cache key
            value: Value to cache (must be JSON-serializable)
            ttl: Time to live in seconds (default: 1 hour)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            ttl = ttl or self.default_ttl
            self.redis_client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Cache set error for key '{key}': {e}")
            return False
    
    def delete(self, key):
        """
        Delete key from cache
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error for key '{key}': {e}")
            return False
    
    def clear_pattern(self, pattern):
        """
        Clear all keys matching pattern
        
        Args:
            pattern: Redis key pattern (e.g., 'embeddings:*')
            
        Returns:
            Number of keys deleted
        """
        if not self.enabled:
            return 0
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except Exception as e:
            print(f"Cache clear pattern error for '{pattern}': {e}")
            return 0
    
    def health_check(self):
        """
        Check if Redis is connected and responsive
        
        Returns:
            True if healthy, False otherwise
        """
        if not self.enabled:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except:
            return False
    
    def get_stats(self):
        """
        Get cache statistics
        
        Returns:
            Dict with cache stats or None if unavailable
        """
        if not self.enabled:
            return None
        
        try:
            info = self.redis_client.info('memory')
            return {
                'enabled': True,
                'memory_used_bytes': info.get('used_memory', 0),
                'memory_used_mb': round(info.get('used_memory', 0) / 1024 / 1024, 2),
                'total_keys': self.redis_client.dbsize()
            }
        except Exception as e:
            print(f"Cache stats error: {e}")
            return {'enabled': False, 'error': str(e)}


# Global cache instance
cache = CacheService()


def cached(ttl=3600, key_prefix=''):
    """
    Decorator to cache function results in Redis
    
    Args:
        ttl: Time to live in seconds (default: 1 hour)
        key_prefix: Prefix for cache keys (recommended for namespacing)
    
    Usage:
        @cached(ttl=3600, key_prefix='embeddings')
        def get_embedding(text, model):
            return expensive_computation(text, model)
    
    The cache key is automatically generated from:
    - key_prefix
    - function name
    - function arguments (args and kwargs)
    
    Returns:
        Decorated function that caches results
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # If cache is disabled, just call the function
            if not cache.enabled:
                return func(*args, **kwargs)
            
            # Generate cache key from function name and arguments
            key_parts = [key_prefix, func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            
            cache_key = hashlib.md5(':'.join(key_parts).encode()).hexdigest()
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result
            
            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        return wrapper
    return decorator
