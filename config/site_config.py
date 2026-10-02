"""
Centralized Site Configuration

Single source of truth for all site-specific information.
Change site name, domain, and organization details in one place.
"""

import os
from typing import Dict, Any


class SiteConfig:
    """
    Centralized configuration for AI agent-ready website.
    All site-specific information is defined here and can be
    overridden via environment variables.
    """
    
    # ========================================
    # SITE IDENTITY
    # ========================================
    SITE_NAME = os.getenv('SITE_NAME', 'Hello World API')
    SITE_DOMAIN = os.getenv('SITE_DOMAIN', 'kiro.fractus.io')
    SITE_URL = os.getenv('SITE_URL', f"https://{SITE_DOMAIN}")
    
    # Site Description
    SITE_DESCRIPTION = os.getenv(
        'SITE_DESCRIPTION',
        'Text transformation and analysis API for AI agents and developers'
    )
    SITE_TAGLINE = os.getenv(
        'SITE_TAGLINE',
        'Multi-language greetings and text processing'
    )
    SITE_KEYWORDS = os.getenv(
        'SITE_KEYWORDS',
        'api, text processing, tokenization, sentiment analysis, language detection, ai agents'
    )
    
    # ========================================
    # API CONFIGURATION
    # ========================================
    API_VERSION = os.getenv('API_VERSION', '1.2.0')
    API_BASE_PATH = '/api'
    
    # ========================================
    # ORGANIZATION
    # ========================================
    ORG_NAME = os.getenv('ORG_NAME', 'Fractus Labs')
    ORG_URL = os.getenv('ORG_URL', 'https://github.com/dstar55')
    
    # ========================================
    # CONTACT & SUPPORT
    # ========================================
    GITHUB_REPO = os.getenv(
        'GITHUB_REPO',
        'https://github.com/dstar55/hello-world-kiro'
    )
    SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@example.com')
    
    # ========================================
    # RATE LIMITING
    # ========================================
    RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', '100'))
    RATE_LIMIT_PER_HOUR = int(os.getenv('RATE_LIMIT_PER_HOUR', '1000'))
    
    # Agent-specific rate limits (higher for known good agents)
    AGENT_RATE_LIMITS = {
        'GPTBot': 200,
        'Claude-Web': 200,
        'PerplexityBot': 150,
        'Googlebot-AI': 200,
    }
    
    # ========================================
    # MONITORING & LOGGING
    # ========================================
    MONITORING_ENABLED = os.getenv('MONITORING_ENABLED', 'true').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    DB_PATH = os.getenv('DB_PATH', 'data/monitoring.db')
    LOG_DIR = os.getenv('LOG_DIR', 'logs')
    
    # ========================================
    # FEATURES
    # ========================================
    MAX_TEXT_LENGTH = int(os.getenv('MAX_TEXT_LENGTH', '10000'))
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    ENABLE_ADMIN_DASHBOARD = os.getenv('ENABLE_ADMIN_DASHBOARD', 'true').lower() == 'true'
    ENABLE_BATCH_PROCESSING = os.getenv('ENABLE_BATCH_PROCESSING', 'true').lower() == 'true'
    ENABLE_AGENT_TRACKING = os.getenv('ENABLE_AGENT_TRACKING', 'true').lower() == 'true'
    
    # ========================================
    # SECURITY
    # ========================================
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'changeme123')
    
    # ========================================
    # REDIS
    # ========================================
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # ========================================
    # HELPER METHODS
    # ========================================
    
    @classmethod
    def get_openapi_info(cls) -> Dict[str, Any]:
        """Generate OpenAPI info block"""
        return {
            "title": cls.SITE_NAME,
            "description": cls.SITE_DESCRIPTION,
            "version": cls.API_VERSION,
            "contact": {
                "name": cls.ORG_NAME,
                "url": cls.ORG_URL,
                "email": cls.SUPPORT_EMAIL
            },
            "license": {
                "name": "MIT",
                "url": f"{cls.GITHUB_REPO}/blob/main/LICENSE"
            }
        }
    
    @classmethod
    def get_schema_org_data(cls) -> Dict[str, Any]:
        """Generate Schema.org structured data"""
        return {
            "@context": "https://schema.org",
            "@type": "WebAPI",
            "name": cls.SITE_NAME,
            "description": cls.SITE_DESCRIPTION,
            "url": cls.SITE_URL,
            "documentation": f"{cls.SITE_URL}/api/docs",
            "provider": {
                "@type": "Organization",
                "name": cls.ORG_NAME,
                "url": cls.ORG_URL
            }
        }
    
    @classmethod
    def get_rate_limit_for_agent(cls, agent_name: str) -> int:
        """Get rate limit for specific agent (requests per minute)"""
        return cls.AGENT_RATE_LIMITS.get(agent_name, cls.RATE_LIMIT_PER_MINUTE)
    
    @classmethod
    def to_dict(cls) -> Dict[str, Any]:
        """Export configuration as dictionary (for debugging)"""
        return {
            'site': {
                'name': cls.SITE_NAME,
                'domain': cls.SITE_DOMAIN,
                'url': cls.SITE_URL,
                'description': cls.SITE_DESCRIPTION
            },
            'api': {
                'version': cls.API_VERSION,
                'base_path': cls.API_BASE_PATH
            },
            'organization': {
                'name': cls.ORG_NAME,
                'url': cls.ORG_URL,
                'github': cls.GITHUB_REPO
            },
            'rate_limiting': {
                'enabled': cls.RATE_LIMIT_ENABLED,
                'per_minute': cls.RATE_LIMIT_PER_MINUTE,
                'per_hour': cls.RATE_LIMIT_PER_HOUR
            },
            'features': {
                'monitoring': cls.MONITORING_ENABLED,
                'batch_processing': cls.ENABLE_BATCH_PROCESSING,
                'agent_tracking': cls.ENABLE_AGENT_TRACKING,
                'admin_dashboard': cls.ENABLE_ADMIN_DASHBOARD
            }
        }
