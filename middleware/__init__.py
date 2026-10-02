"""
Middleware package for Flask application
"""

from .monitoring_middleware import init_monitoring_middleware

__all__ = ['init_monitoring_middleware']
