"""
Discovery Routes for AI Agents

Dynamic generation of machine-readable files for AI agent discovery:
- /llms.txt - AI agent discovery file
- /robots.txt - Crawler guidelines
- /sitemap.xml - Site structure
- /.well-known/mcp.json - Model Context Protocol card
"""

from flask import Blueprint, Response
from datetime import datetime
from config import SiteConfig

discovery_bp = Blueprint('discovery', __name__)


@discovery_bp.route('/llms.txt')
def llms_txt():
    """
    Generate llms.txt file for AI agent discovery.
    
    This file tells AI agents what your site offers and how to use it.
    Dynamically generated from SiteConfig to ensure consistency.
    """
    content = f"""# {SiteConfig.SITE_NAME} - {SiteConfig.SITE_DOMAIN}

## Purpose
{SiteConfig.SITE_DESCRIPTION}

## What We Offer

### Text Transformation API
High-performance text processing operations designed for AI agents and developers.

**Base URL:** {SiteConfig.SITE_URL}{SiteConfig.API_BASE_PATH}/text

**Available Operations:**

**Group A: Instant Operations (< 10ms)**
1. Base64 Encode/Decode - Convert text to/from Base64
2. Hash Generation - MD5, SHA1, SHA256, SHA512 cryptographic hashes
3. Text Normalization - Clean and standardize text
4. Text Statistics - Character, word, sentence counts and reading time
5. Entity Extraction - Extract URLs, emails, phone numbers
6. Case Conversion - upper, lower, title, camel, pascal, snake, kebab

**Group B: ML Operations**
7. Tokenization - Count tokens for GPT-4, GPT-3.5, Claude models
8. Language Detection - Identify text language with confidence scores
9. Sentiment Analysis - Analyze text sentiment (positive/negative/neutral)

### Currency Converter
Real-time currency conversion with live exchange rates.

**Endpoint:** {SiteConfig.SITE_URL}/api/convert
**Supported Currencies:** USD, EUR, GBP, TRY, RUB
**Update Frequency:** Multiple times per day
**Rate Source:** exchangerate-api.com

### Multi-Language Interface
Hello World greetings in 8 languages:
- English, German, French, Croatian, Spanish, Turkish, Portuguese, Russian

## Documentation

**Complete API Documentation:** {SiteConfig.SITE_URL}/api/docs
**OpenAPI Specification:** {SiteConfig.SITE_URL}/openapi.json
**API Capabilities:** {SiteConfig.SITE_URL}/api/capabilities
**Interactive Testing:** {SiteConfig.SITE_URL}/api-test
**GitHub Repository:** {SiteConfig.GITHUB_REPO}

## Rate Limits

- **Standard:** {SiteConfig.RATE_LIMIT_PER_MINUTE} requests per minute per IP
- **AI Agents (GPTBot, Claude-Web, etc.):** {SiteConfig.get_rate_limit_for_agent('GPTBot')} requests per minute
- **Burst protection:** Enabled
- **Contact for higher limits:** {SiteConfig.SUPPORT_EMAIL}

## Usage Examples

### cURL Example
```bash
curl -X POST {SiteConfig.SITE_URL}/api/text/tokenize \\
  -H "Content-Type: application/json" \\
  -d '{{"text": "Hello World", "model": "gpt-4"}}'
```

### Python Example
```python
import requests

response = requests.post(
    '{SiteConfig.SITE_URL}/api/text/tokenize',
    json={{"text": "Hello World", "model": "gpt-4"}}
)
print(response.json())
```

### JavaScript Example
```javascript
fetch('{SiteConfig.SITE_URL}/api/text/tokenize', {{
  method: 'POST',
  headers: {{'Content-Type': 'application/json'}},
  body: JSON.stringify({{text: 'Hello World', model: 'gpt-4'}})
}})
.then(r => r.json())
.then(data => console.log(data));
```

## Features for AI Agents

✅ **Machine-readable API documentation** (OpenAPI 3.0)
✅ **Consistent JSON responses** with error handling
✅ **Fast response times** (< 50ms average)
✅ **CORS enabled** for browser-based agents
✅ **Batch processing** available at /api/batch
✅ **Request tracking** and analytics
✅ **No authentication required** (free tier)

## Technical Details

**API Version:** {SiteConfig.API_VERSION}
**Response Format:** JSON
**Character Encoding:** UTF-8
**Maximum Text Length:** {SiteConfig.MAX_TEXT_LENGTH:,} characters
**Cache:** Redis-backed for ML operations
**Uptime:** 99.9% (monitored)

## Contact & Support

**Organization:** {SiteConfig.ORG_NAME}
**Website:** {SiteConfig.ORG_URL}
**Email:** {SiteConfig.SUPPORT_EMAIL}
**GitHub:** {SiteConfig.GITHUB_REPO}
**Issues:** {SiteConfig.GITHUB_REPO}/issues

## Attribution

When using this API in your AI agent or application, please consider:
- Citing {SiteConfig.SITE_NAME} in your documentation
- Linking to {SiteConfig.SITE_URL}
- Respecting rate limits

## Updates

This file is dynamically generated and always reflects current capabilities.
Last generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

---

Built for AI agents, by developers who understand your needs.
"""
    
    return Response(content, mimetype='text/plain; charset=utf-8')


@discovery_bp.route('/robots.txt')
def robots_txt():
    """
    Generate robots.txt with AI agent-specific guidelines.
    
    Allows all agents but sets crawl delays and specific rules.
    """
    content = f"""# Robots.txt for {SiteConfig.SITE_DOMAIN}
# Generated: {datetime.now().strftime('%Y-%m-%d')}

# Allow all agents
User-agent: *
Allow: /
Allow: {SiteConfig.API_BASE_PATH}/
Allow: /llms.txt
Allow: /openapi.json
Allow: /.well-known/
Crawl-delay: 1

# Sitemap location
Sitemap: {SiteConfig.SITE_URL}/sitemap.xml

# API documentation - important for AI agents
Allow: /api/docs
Allow: /api/capabilities
Allow: /api-test

# Static assets
Allow: /static/

# Disallow private/admin areas (when implemented)
Disallow: /admin/
Disallow: /data/
Disallow: /logs/

# AI-specific agents - higher crawl rate allowed
User-agent: GPTBot
User-agent: ChatGPT-User
Allow: /
Crawl-delay: 0.5

User-agent: Claude-Web
User-agent: anthropic-ai
Allow: /
Crawl-delay: 0.5

User-agent: PerplexityBot
Allow: /
Crawl-delay: 0.5

User-agent: Googlebot-AI
User-agent: Google-Extended
Allow: /
Crawl-delay: 0.5

User-agent: Meta-ExternalAgent
User-agent: FacebookBot
Allow: /
Crawl-delay: 0.5

User-agent: Applebot-Extended
Allow: /
Crawl-delay: 0.5

# AI training bots - allow with standard delay
User-agent: CCBot
User-agent: cohere-ai
User-agent: AI2Bot
Allow: /
Crawl-delay: 1

# Aggressive crawlers - higher delay
User-agent: archive.org_bot
User-agent: ia_archiver
Crawl-delay: 5

# Block known bad bots
User-agent: SemrushBot
User-agent: AhrefsBot
User-agent: MJ12bot
Disallow: /

# Special note for AI agents
# For best results, read /llms.txt first
# OpenAPI spec available at /openapi.json
# Rate limits: {SiteConfig.RATE_LIMIT_PER_MINUTE} req/min (standard), {SiteConfig.get_rate_limit_for_agent('GPTBot')} req/min (AI agents)
"""
    
    return Response(content, mimetype='text/plain; charset=utf-8')


@discovery_bp.route('/sitemap.xml')
def sitemap_xml():
    """
    Generate XML sitemap with all pages and API endpoints.
    
    Helps search engines and AI agents discover all content.
    """
    # Define all routes with priority and change frequency
    routes = [
        # Main pages
        {'loc': '/', 'priority': '1.0', 'changefreq': 'weekly'},
        
        # Language pages
        {'loc': '/de', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/fr', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/hr', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/es', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/tr', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/pt', 'priority': '0.9', 'changefreq': 'monthly'},
        {'loc': '/ru', 'priority': '0.9', 'changefreq': 'monthly'},
        
        # API documentation
        {'loc': '/api/docs', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': '/api-test', 'priority': '0.8', 'changefreq': 'weekly'},
        
        # Discovery files
        {'loc': '/llms.txt', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': '/openapi.json', 'priority': '0.9', 'changefreq': 'weekly'},
        {'loc': '/.well-known/mcp.json', 'priority': '0.8', 'changefreq': 'weekly'},
        
        # Health and info
        {'loc': '/health', 'priority': '0.5', 'changefreq': 'always'},
        {'loc': '/api', 'priority': '0.7', 'changefreq': 'weekly'},
    ]
    
    # Build XML
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    lastmod = datetime.now().strftime('%Y-%m-%d')
    
    for route in routes:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>{SiteConfig.SITE_URL}{route["loc"]}</loc>')
        xml_content.append(f'    <lastmod>{lastmod}</lastmod>')
        xml_content.append(f'    <changefreq>{route["changefreq"]}</changefreq>')
        xml_content.append(f'    <priority>{route["priority"]}</priority>')
        xml_content.append('  </url>')
    
    xml_content.append('</urlset>')
    
    return Response('\n'.join(xml_content), mimetype='application/xml; charset=utf-8')


@discovery_bp.route('/.well-known/mcp.json')
def mcp_json():
    """
    Generate Model Context Protocol (MCP) card.
    
    Enables modern AI assistants to discover and use your API.
    """
    import json
    
    mcp_data = {
        "mcp_version": "1.0",
        "name": SiteConfig.SITE_NAME,
        "description": SiteConfig.SITE_DESCRIPTION,
        "api": {
            "name": f"{SiteConfig.SITE_NAME} Text API",
            "version": SiteConfig.API_VERSION,
            "base_url": f"{SiteConfig.SITE_URL}{SiteConfig.API_BASE_PATH}",
            "documentation_url": f"{SiteConfig.SITE_URL}/api/docs",
            "openapi_url": f"{SiteConfig.SITE_URL}/openapi.json",
            "capabilities_url": f"{SiteConfig.SITE_URL}/api/capabilities"
        },
        "endpoints": {
            "text_processing": {
                "base_url": f"{SiteConfig.SITE_URL}{SiteConfig.API_BASE_PATH}/text",
                "operations": [
                    "base64/encode",
                    "base64/decode",
                    "hash",
                    "normalize",
                    "stats",
                    "extract",
                    "case-convert",
                    "tokenize",
                    "detect-language",
                    "sentiment"
                ]
            },
            "currency": {
                "base_url": f"{SiteConfig.SITE_URL}/api/convert",
                "description": "Real-time currency conversion"
            }
        },
        "rate_limits": {
            "default": {
                "requests_per_minute": SiteConfig.RATE_LIMIT_PER_MINUTE,
                "requests_per_hour": SiteConfig.RATE_LIMIT_PER_HOUR
            },
            "ai_agents": {
                "requests_per_minute": SiteConfig.get_rate_limit_for_agent('GPTBot'),
                "description": "Higher limits for known AI agents (GPTBot, Claude-Web, etc.)"
            }
        },
        "features": {
            "cors_enabled": True,
            "batch_processing": SiteConfig.ENABLE_BATCH_PROCESSING,
            "caching": SiteConfig.CACHE_ENABLED,
            "authentication_required": False
        },
        "contact": {
            "organization": SiteConfig.ORG_NAME,
            "website": SiteConfig.ORG_URL,
            "email": SiteConfig.SUPPORT_EMAIL,
            "github": SiteConfig.GITHUB_REPO
        },
        "metadata": {
            "keywords": SiteConfig.SITE_KEYWORDS.split(', '),
            "categories": ["api", "text-processing", "ai-tools", "nlp"],
            "last_updated": datetime.now().isoformat()
        }
    }
    
    return Response(
        json.dumps(mcp_data, indent=2),
        mimetype='application/json; charset=utf-8'
    )
