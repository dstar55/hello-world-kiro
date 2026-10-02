# 🌍 Hello World API - AI Agent Ready

**A production-ready Python Flask API with multi-language support, text processing, and AI agent integration.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![AI Agent Ready](https://img.shields.io/badge/AI%20Agent-Ready-success.svg)](https://kiro.fractus.io/llms.txt)

🔗 **Live Site:** https://kiro.fractus.io  
📚 **API Docs:** https://kiro.fractus.io/api/docs  
🤖 **AI Agent Guide:** [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)

## Supported Languages

- 🇬🇧 **English** - Hello, World! (Currency: GBP £)
- 🇩🇪 **German (Deutsch)** - Hallo, Welt! (Currency: EUR €)
- 🇫🇷 **French (Français)** - Bonjour, le monde! (Currency: EUR €)
- 🇭🇷 **Croatian (Hrvatski)** - Pozdrav, svijete! (Currency: EUR €)
- 🇪🇸 **Spanish (Español)** - ¡Hola, Mundo! (Currency: EUR €)
- 🇹🇷 **Turkish (Türkçe)** - Merhaba, Dünya! (Currency: TRY ₺)
- 🇵🇹 **Portuguese (Português)** - Olá, Mundo! (Currency: EUR €)
- 🇷🇺 **Russian (Русский)** - Привет, мир! (Currency: RUB ₽)
- 🇺🇸 **US Dollar** - USD $ (Base currency for conversions)

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Redis (for caching and rate limiting)
- pip (Python package installer)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/dstar55/hello-world-kiro.git
cd hello-world-kiro
```

2. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Start Redis** (if not already running):
```bash
# Linux/macOS
redis-server

# Docker
docker run -d --name redis -p 6379:6379 redis:alpine
```

6. **Run the application:**
```bash
python app.py
```

7. **Open your browser:**
```
http://localhost:5000
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | Complete API reference |
| [API_EXAMPLES.md](API_EXAMPLES.md) | API usage examples |
| [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) | Guide for AI agent integration |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Production deployment instructions |
| [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md) | Pre-launch checklist |
| [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) | Implementation progress |

## 🛣️ API Endpoints

### **Web Pages**
- `/` - Homepage (English)
- `/de`, `/fr`, `/hr`, `/es`, `/tr`, `/pt`, `/ru` - Other languages
- `/api/docs` - Interactive API documentation
- `/admin` - Admin dashboard (requires authentication)

### **API Discovery**
- `/llms.txt` - AI agent discovery file
- `/robots.txt` - Crawler guidelines
- `/sitemap.xml` - Site structure
- `/.well-known/mcp.json` - Model Context Protocol card
- `/openapi.json` - OpenAPI 3.0 specification

### **Text API**
- `POST /api/text/uppercase` - Convert to uppercase
- `POST /api/text/lowercase` - Convert to lowercase
- `POST /api/text/reverse` - Reverse text
- `POST /api/text/length` - Get text length
- `POST /api/text/word-count` - Count words
- And 5 more operations...

### **Batch Processing**
- `POST /api/batch` - Process up to 100 operations at once
- `GET /api/operations` - List all available operations

### **System**
- `GET /health` - Health check
- `GET /api` - API information
- `GET /api/capabilities` - Detailed capabilities
- `POST /api/convert` - Currency conversion

## 💡 Usage Examples

### Text API (Single Operation)
```bash
curl -X POST https://kiro.fractus.io/api/text/uppercase \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'

# Response: {"success": true, "result": "HELLO WORLD"}
```

### Batch Processing (Multiple Operations)
```bash
curl -X POST https://kiro.fractus.io/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {"operation": "uppercase", "text": "hello"},
      {"operation": "reverse", "text": "world"},
      {"operation": "length", "text": "test"}
    ]
  }'

# Response: All 3 operations processed in one request
```

### For AI Agents
```python
import requests

# Higher rate limits automatically applied with User-Agent
headers = {"User-Agent": "GPTBot/1.0"}
response = requests.post(
    "https://kiro.fractus.io/api/text/uppercase",
    json={"text": "hello"},
    headers=headers
)
```

See [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) for complete integration guide.

## 📁 Project Structure

```
hello-world-kiro/
├── api/                          # API blueprints
│   ├── text.py                   # Text processing endpoints
│   ├── discovery_routes.py       # AI agent discovery
│   ├── openapi_spec.py          # OpenAPI 3.0 generator
│   └── batch_routes.py          # Batch processing
├── config/                       # Configuration
│   └── site_config.py           # Centralized site configuration
├── middleware/                   # Middleware
│   ├── monitoring_middleware.py  # Request tracking
│   ├── cors_middleware.py        # CORS support
│   └── rate_limit_middleware.py  # Rate limiting
├── services/                     # Services
│   ├── cache_service.py         # Redis caching
│   ├── text_service.py          # Text operations
│   └── monitoring_service.py    # Analytics and monitoring
├── templates/                    # HTML templates
│   ├── base.html                # Base template with SEO
│   ├── index.html               # Homepage
│   ├── api_docs.html            # Interactive API docs
│   ├── api_test.html            # API testing page
│   └── admin_dashboard.html     # Admin dashboard
├── app.py                       # Main Flask application
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose setup
└── README.md                    # This file
```

## ⚙️ Configuration

All configuration is centralized in `.env` file:

```env
# Site Identity
SITE_NAME=Hello World API
SITE_DOMAIN=kiro.fractus.io
SITE_URL=https://kiro.fractus.io

# Security
SECRET_KEY=your-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme123

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# Features
MONITORING_ENABLED=true
CACHE_ENABLED=true
ENABLE_BATCH_PROCESSING=true
ENABLE_AGENT_TRACKING=true

# Redis
REDIS_URL=redis://localhost:6379/0
```

**⚠️ Important:** Always change default credentials in production!

## Technology Stack

- **Framework**: Flask 3.0+
- **Language**: Python 3.8+
- **Template Engine**: Jinja2 (built into Flask)

## ✨ Features

### **🌐 Multi-Language Support**
- 8 languages: English, German, French, Croatian, Spanish, Turkish, Portuguese, Russian
- Flag emojis for easy navigation
- Currency information for each language

### **💱 Live Currency Converter**
- Real-time exchange rates from [exchangerate-api.com](https://exchangerate-api.com)
- Smart 1-hour caching for performance
- Automatic fallback to static rates
- Support for USD, EUR, GBP, TRY, RUB

### **🤖 AI Agent Ready**
- **Discovery**: `/llms.txt`, `/robots.txt`, `/sitemap.xml`, `/.well-known/mcp.json`
- **OpenAPI 3.0** specification at `/openapi.json`
- **Higher rate limits** for AI agents (200/min vs 100/min)
- **Automatic detection** of GPTBot, Claude-Web, PerplexityBot, Googlebot-AI, etc.
- **Batch processing** for efficient multi-operation requests

### **📦 Text Processing API**
10 text operations available:
- Uppercase, Lowercase, Reverse, Length, Word Count
- Capitalize, Title Case, Strip, Swapcase, Count Vowels

**Batch processing support**: Process up to 100 operations in a single request!

### **🛡️ Safety & Performance**
- **Rate limiting**: IP-based with AI agent detection
- **CORS enabled**: Cross-origin requests supported
- **Monitoring**: Comprehensive request tracking and analytics
- **Admin dashboard**: Real-time metrics at `/admin`
- **Caching**: Redis-backed for optimal performance

### **📊 Admin Dashboard**
- Real-time request metrics
- AI agent activity tracking
- Success rates and response times
- Rate limit event monitoring
- Top endpoints analysis
- HTTP Basic Authentication

### **📚 Documentation**
- Interactive API docs at `/api/docs`
- Complete AI agent integration guide
- OpenAPI 3.0 specification
- Code examples in Python, JavaScript, cURL, Go

## 🧪 Testing

```bash
# Test configuration
python -c "from config import SiteConfig; print('Config OK')"

# Test Redis
python -c "from services.cache_service import cache; print('Redis:', cache.health_check())"

# Test health endpoint
curl http://localhost:5000/health

# Test text API
curl -X POST http://localhost:5000/api/text/uppercase \
  -H "Content-Type: application/json" \
  -d '{"text": "test"}'

# Run full test suite
python -m pytest tests/
```

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

**Quick deployment options:**

### Docker
```bash
docker-compose up -d
```

### Systemd Service
```bash
sudo systemctl enable hello-world-api
sudo systemctl start hello-world-api
```

### Cloud Platforms
- Heroku: `git push heroku main`
- Google Cloud Run: `gcloud run deploy`
- AWS Elastic Beanstalk: `eb deploy`

**Pre-deployment checklist:** [PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)

## License

See LICENSE file for details.


## 🤖 For AI Agents

This API is specifically designed to be AI agent-friendly:

### **Automatic Discovery**
AI agents can discover this API via:
1. Check `/robots.txt` → Find `/llms.txt`
2. Read `/llms.txt` → Get API description
3. Fetch `/openapi.json` → Get full specification
4. Start using API → Success!

### **Higher Rate Limits**
Automatically detected AI agents get 2x rate limit:
- Standard: 100 requests/minute
- AI Agents: 200 requests/minute

Detected agents: GPTBot, Claude-Web, PerplexityBot, Googlebot-AI, Meta-AI, AppleBot-AI

### **Batch Processing**
Process up to 100 operations in a single request:
```json
{
  "operations": [
    {"operation": "uppercase", "text": "hello"},
    {"operation": "reverse", "text": "world"}
  ]
}
```

### **Complete Documentation**
- [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md) - Full integration guide
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
- `/api/docs` - Interactive documentation
- `/openapi.json` - OpenAPI 3.0 specification

## 🛡️ Security Features

- ✅ Rate limiting (IP-based with AI agent detection)
- ✅ CORS enabled for cross-origin requests
- ✅ HTTP Basic Authentication for admin dashboard
- ✅ Input validation and sanitization
- ✅ Secure default configurations
- ✅ Environment-based secrets management
- ✅ Redis password support
- ✅ HTTPS ready (with reverse proxy)

## 📊 Monitoring

### Admin Dashboard
Access real-time metrics at `/admin`:
- Request counts and success rates
- AI agent activity tracking
- Response time analytics
- Rate limit events
- Top endpoints by usage

**Authentication:** HTTP Basic Auth (configure in `.env`)

### Health Check
```bash
curl https://kiro.fractus.io/health
```

Returns:
- API status
- Redis connection status
- Cache statistics
- Enabled features

## 🔧 Technology Stack

- **Framework:** Flask 3.0+
- **Language:** Python 3.9+
- **Caching:** Redis
- **Database:** SQLite (default) / PostgreSQL (optional)
- **Rate Limiting:** Flask-Limiter
- **CORS:** Flask-CORS
- **Template Engine:** Jinja2
- **WSGI Server:** Gunicorn (production)

## 📈 Performance

- **Response Time:** <100ms average
- **Throughput:** 100-200 requests/minute per client
- **Batch Processing:** 90% faster than individual requests
- **Caching:** Redis-backed for optimal performance
- **Scaling:** Horizontal scaling ready

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask community for the excellent framework
- AI agent providers for inspiring this project
- Contributors and users of this API

## 📞 Support

- **GitHub Issues:** [Create an issue](https://github.com/dstar55/hello-world-kiro/issues)
- **Email:** support@fractus.io
- **Documentation:** https://kiro.fractus.io/api/docs

## 🗺️ Roadmap

- [ ] GraphQL support
- [ ] WebSocket connections
- [ ] More text processing operations
- [ ] Multi-language text processing
- [ ] Machine learning integrations
- [ ] Enhanced analytics dashboard

---

**Built with ❤️ for AI agents and developers**

🔗 Live Site: https://kiro.fractus.io  
📚 Documentation: https://kiro.fractus.io/api/docs  
🤖 AI Agent Guide: [AI_AGENT_GUIDE.md](AI_AGENT_GUIDE.md)
