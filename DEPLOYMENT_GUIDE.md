# 🚀 Deployment Guide

**Complete guide for deploying {{ site_config.SITE_NAME }} to production**

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Database Setup](#database-setup)
- [Redis Setup](#redis-setup)
- [Application Configuration](#application-configuration)
- [Deployment Options](#deployment-options)
- [Security Checklist](#security-checklist)
- [Monitoring Setup](#monitoring-setup)
- [Troubleshooting](#troubleshooting)

---

## ✅ Prerequisites

Before deploying, ensure you have:

- [ ] Python 3.9 or higher
- [ ] Redis server (for caching and rate limiting)
- [ ] Docker (optional, for containerized deployment)
- [ ] Git (for version control)
- [ ] Domain name configured with DNS
- [ ] SSL certificate (Let's Encrypt recommended)

---

## 🔧 Environment Setup

### **1. Clone the Repository**

```bash
git clone https://github.com/dstar55/hello-world-kiro.git
cd hello-world-kiro
```

### **2. Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Create Environment File**

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your production values:

```env
# Site Configuration
SITE_NAME=Hello World API
SITE_DOMAIN=kiro.fractus.io
SITE_URL=https://kiro.fractus.io

# Organization
ORG_NAME=Fractus Labs
SUPPORT_EMAIL=support@fractus.io

# Security (IMPORTANT: Change these!)
SECRET_KEY=your-super-secret-key-change-this
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your-secure-password-change-this

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# Redis
REDIS_URL=redis://localhost:6379/0

# Monitoring
MONITORING_ENABLED=true
LOG_LEVEL=INFO
DB_PATH=data/monitoring.db
LOG_DIR=logs

# Features
MAX_TEXT_LENGTH=10000
CACHE_ENABLED=true
ENABLE_BATCH_PROCESSING=true
ENABLE_AGENT_TRACKING=true
ENABLE_ADMIN_DASHBOARD=true
```

---

## 🗄️ Database Setup

### **SQLite (Default - Simple)**

SQLite database is created automatically on first run.

```bash
# Create data directory
mkdir -p data

# Database will be created at: data/monitoring.db
```

### **PostgreSQL (Production - Scalable)**

For high-traffic production environments:

1. **Install PostgreSQL:**
```bash
sudo apt-get install postgresql postgresql-contrib
```

2. **Create Database:**
```bash
sudo -u postgres psql
CREATE DATABASE hello_world_api;
CREATE USER apiuser WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE hello_world_api TO apiuser;
\q
```

3. **Update Configuration:**
```env
DB_PATH=postgresql://apiuser:your-password@localhost/hello_world_api
```

---

## 🔴 Redis Setup

### **Linux (Ubuntu/Debian)**

```bash
sudo apt-get update
sudo apt-get install redis-server

# Start Redis
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

### **macOS**

```bash
brew install redis

# Start Redis
brew services start redis

# Verify
redis-cli ping
```

### **Docker**

```bash
docker run -d --name redis -p 6379:6379 redis:alpine
```

### **Production Redis Configuration**

Edit `/etc/redis/redis.conf`:

```conf
# Security
requirepass your-redis-password
bind 127.0.0.1

# Performance
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000
```

Update `.env`:
```env
REDIS_URL=redis://:your-redis-password@localhost:6379/0
```

---

## ⚙️ Application Configuration

### **1. Generate Secret Key**

```python
python -c "import secrets; print(secrets.token_hex(32))"
```

Use the output as your `SECRET_KEY` in `.env`.

### **2. Configure Admin Credentials**

**⚠️ IMPORTANT:** Change default admin credentials!

```env
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-secure-password-at-least-16-chars
```

### **3. Test Configuration**

```bash
python -c "from config import SiteConfig; print(SiteConfig.to_dict())"
```

Verify all settings are correct.

---

## 🚀 Deployment Options

### **Option 1: Docker (Recommended)**

#### **Build Docker Image**

```bash
docker build -t hello-world-api:latest .
```

#### **Run with Docker Compose**

```bash
# Start all services (app + redis)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

`docker-compose.yml` example:
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - REDIS_URL=redis://redis:6379/0
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

### **Option 2: Systemd Service (Linux)**

#### **Create Service File**

`/etc/systemd/system/hello-world-api.service`:

```ini
[Unit]
Description=Hello World API
After=network.target redis.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/hello-world-kiro
Environment="PATH=/var/www/hello-world-kiro/venv/bin"
ExecStart=/var/www/hello-world-kiro/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### **Enable and Start Service**

```bash
sudo systemctl daemon-reload
sudo systemctl enable hello-world-api
sudo systemctl start hello-world-api
sudo systemctl status hello-world-api
```

### **Option 3: Cloud Platforms**

#### **Heroku**

```bash
# Create app
heroku create your-app-name

# Add Redis
heroku addons:create heroku-redis:hobby-dev

# Configure environment
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ADMIN_PASSWORD=your-password

# Deploy
git push heroku main
```

#### **AWS (EC2 + Elastic Beanstalk)**

1. Install EB CLI: `pip install awsebcli`
2. Initialize: `eb init`
3. Create environment: `eb create production`
4. Deploy: `eb deploy`

#### **Google Cloud Run**

```bash
# Build and deploy
gcloud run deploy hello-world-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🔒 Security Checklist

Before going to production:

### **Critical**
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Change `ADMIN_PASSWORD` to a secure password
- [ ] Change `ADMIN_USERNAME` from default `admin`
- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set `DEBUG=False` in production
- [ ] Restrict Redis access (bind to localhost or use password)
- [ ] Configure firewall rules (allow only 80, 443, 22)

### **Important**
- [ ] Set up regular database backups
- [ ] Configure log rotation
- [ ] Enable monitoring and alerting
- [ ] Set up rate limiting properly
- [ ] Review and restrict file permissions
- [ ] Update dependencies regularly
- [ ] Enable Redis persistence
- [ ] Configure CORS appropriately

### **Recommended**
- [ ] Set up fail2ban for SSH protection
- [ ] Configure automated security updates
- [ ] Implement database encryption at rest
- [ ] Set up Web Application Firewall (WAF)
- [ ] Configure DDoS protection
- [ ] Implement intrusion detection
- [ ] Set up log aggregation (ELK/Splunk)

---

## 📊 Monitoring Setup

### **Application Monitoring**

Access admin dashboard:
```
https://kiro.fractus.io/admin
```

Monitor:
- Request counts
- Success rates
- Response times
- AI agent activity
- Rate limit events

### **System Monitoring**

Install monitoring tools:

```bash
# Prometheus + Grafana
docker-compose -f monitoring-stack.yml up -d

# Or install directly
sudo apt-get install prometheus grafana
```

### **Log Monitoring**

```bash
# View application logs
tail -f logs/api_requests.log

# View systemd logs
journalctl -u hello-world-api -f

# View Docker logs
docker logs -f hello-world-api
```

### **Uptime Monitoring**

Set up external monitoring:
- [UptimeRobot](https://uptimerobot.com/) (free)
- [Pingdom](https://www.pingdom.com/)
- [StatusCake](https://www.statuscake.com/)

Monitor endpoints:
- `https://kiro.fractus.io/health` (API health)
- `https://kiro.fractus.io/` (Main site)

### **Alerts**

Configure alerts for:
- API downtime
- High error rates (>5%)
- High response times (>1000ms)
- Rate limit spikes
- Redis connection failures
- Disk space low (<10%)

---

## 🔥 Production WSGI Server

**⚠️ Never use Flask's built-in server in production!**

### **Gunicorn (Recommended)**

```bash
pip install gunicorn

# Run with 4 workers
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app

# With better settings
gunicorn --bind 0.0.0.0:5000 \
  --workers 4 \
  --worker-class sync \
  --timeout 120 \
  --keep-alive 5 \
  --max-requests 1000 \
  --max-requests-jitter 100 \
  --access-logfile logs/access.log \
  --error-logfile logs/error.log \
  app:app
```

### **uWSGI (Alternative)**

```bash
pip install uwsgi

uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

---

## 🌐 Reverse Proxy Setup

### **Nginx (Recommended)**

`/etc/nginx/sites-available/hello-world-api`:

```nginx
upstream hello_world_api {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name kiro.fractus.io;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name kiro.fractus.io;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/kiro.fractus.io/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/kiro.fractus.io/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # Logging
    access_log /var/log/nginx/hello-world-api.access.log;
    error_log /var/log/nginx/hello-world-api.error.log;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/m;
    limit_req zone=api_limit burst=20 nodelay;
    
    location / {
        proxy_pass http://hello_world_api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Static files (if any)
    location /static {
        alias /var/www/hello-world-kiro/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/hello-world-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### **SSL Certificate (Let's Encrypt)**

```bash
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d kiro.fractus.io

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

---

## 🧪 Testing Before Deploy

```bash
# 1. Run unit tests
python -m pytest tests/

# 2. Check configuration
python -c "from config import SiteConfig; print('Config OK')"

# 3. Test Redis connection
python -c "from services.cache_service import cache; print('Redis:', cache.health_check())"

# 4. Test database
python -c "from services.monitoring_service import monitoring; print('Database OK')"

# 5. Test application
curl http://localhost:5000/health
```

---

## 🔄 Backup Strategy

### **Database Backup**

```bash
# SQLite backup script
#!/bin/bash
BACKUP_DIR="/backups/hello-world-api"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
sqlite3 data/monitoring.db ".backup '$BACKUP_DIR/monitoring_$DATE.db'"

# Keep last 30 days
find $BACKUP_DIR -name "monitoring_*.db" -mtime +30 -delete
```

Add to cron:
```bash
0 2 * * * /path/to/backup-script.sh
```

### **Redis Backup**

Redis automatically saves RDB snapshots based on configuration.

Manual backup:
```bash
redis-cli SAVE
cp /var/lib/redis/dump.rdb /backups/redis/dump_$(date +%Y%m%d).rdb
```

---

## 🐛 Troubleshooting

### **Application Won't Start**

```bash
# Check logs
journalctl -u hello-world-api -n 50

# Check if port is in use
sudo netstat -tulpn | grep 5000

# Check environment variables
printenv | grep SITE
```

### **Redis Connection Failed**

```bash
# Check Redis status
sudo systemctl status redis-server

# Test connection
redis-cli ping

# Check Redis logs
tail -f /var/log/redis/redis-server.log
```

### **High Response Times**

```bash
# Check worker count
ps aux | grep gunicorn

# Monitor system resources
htop

# Check Redis performance
redis-cli --latency

# Review slow queries in logs
grep "response_time_ms" logs/api_requests.log | sort -t: -k5 -n | tail
```

### **Rate Limiting Issues**

```bash
# Check Redis keys
redis-cli KEYS "LIMITER:*"

# Clear rate limits (if needed)
redis-cli KEYS "LIMITER:*" | xargs redis-cli DEL

# Monitor rate limit events
tail -f logs/api_requests.log | grep "rate_limit"
```

---

## 📈 Scaling Recommendations

### **Vertical Scaling (Single Server)**
- Start: 2 CPU, 4GB RAM
- Medium: 4 CPU, 8GB RAM
- Large: 8 CPU, 16GB RAM

### **Horizontal Scaling (Multiple Servers)**

1. **Load Balancer** (Nginx/HAProxy)
2. **Multiple App Servers** (Gunicorn on each)
3. **Shared Redis** (Redis Cluster or AWS ElastiCache)
4. **Shared Database** (PostgreSQL with replication)

### **CDN Integration**

Use CDN for static assets and API caching:
- CloudFlare (recommended)
- AWS CloudFront
- Fastly

---

## ✅ Post-Deployment Checklist

After deploying to production:

- [ ] Verify site loads: https://kiro.fractus.io
- [ ] Test API endpoint: https://kiro.fractus.io/api
- [ ] Check health: https://kiro.fractus.io/health
- [ ] Test admin dashboard: https://kiro.fractus.io/admin
- [ ] Verify SSL certificate (no browser warnings)
- [ ] Test rate limiting (make 101 requests quickly)
- [ ] Check Redis connection in dashboard
- [ ] Test AI agent detection (set User-Agent: GPTBot/1.0)
- [ ] Review logs for errors
- [ ] Set up monitoring alerts
- [ ] Schedule regular backups
- [ ] Document admin credentials securely
- [ ] Share API documentation with team
- [ ] Update DNS if needed
- [ ] Test from different locations/ISPs

---

## 🎉 Success!

Your Hello World API is now deployed and ready for AI agents!

**Next Steps:**
1. Share the API with AI agents: https://kiro.fractus.io/llms.txt
2. Monitor usage: https://kiro.fractus.io/admin
3. Review analytics regularly
4. Update dependencies monthly
5. Scale as needed

**Support:**
- GitHub: https://github.com/dstar55/hello-world-kiro
- Email: support@fractus.io

---

*Last updated: 2026-10-02*
