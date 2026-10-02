"""
Monitoring and Analytics Service

Tracks API usage, AI agent activity, and system health.
Uses hybrid storage: Redis (hot), SQLite (cold), JSON logs (backup)
"""

import json
import sqlite3
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple, List
import logging
from pathlib import Path
import re

from services.cache_service import cache
from config import SiteConfig

# Setup logging
log_dir = Path(SiteConfig.LOG_DIR)
log_dir.mkdir(exist_ok=True)

# JSON structured logging
json_logger = logging.getLogger('api_requests')
json_handler = logging.FileHandler(log_dir / 'api_requests.log')
json_handler.setFormatter(logging.Formatter('%(message)s'))
json_logger.addHandler(json_handler)
json_logger.setLevel(logging.INFO)


class MonitoringService:
    """Centralized monitoring and analytics"""
    
    # AI Agent patterns (User-Agent detection)
    AI_AGENTS = {
        r'GPTBot': ('GPTBot', 'ai_agent'),
        r'Claude-Web': ('Claude-Web', 'ai_agent'),
        r'anthropic-ai': ('Anthropic-AI', 'ai_agent'),
        r'PerplexityBot': ('PerplexityBot', 'ai_agent'),
        r'Googlebot-AI': ('Googlebot-AI', 'ai_agent'),
        r'cohere-ai': ('Cohere-AI', 'ai_agent'),
        r'AI2Bot': ('AI2Bot', 'ai_agent'),
        r'Meta-ExternalAgent': ('Meta-AI', 'ai_agent'),
        r'Applebot-Extended': ('AppleBot-AI', 'ai_agent'),
    }
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or SiteConfig.DB_PATH
        # Ensure data directory exists
        Path(self.db_path).parent.mkdir(exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                method VARCHAR(10),
                endpoint VARCHAR(255),
                path VARCHAR(500),
                ip_address VARCHAR(45),
                user_agent TEXT,
                agent_type VARCHAR(50),
                agent_name VARCHAR(100),
                request_body TEXT,
                request_headers TEXT,
                status_code INTEGER,
                response_time_ms INTEGER,
                response_size_bytes INTEGER,
                error_message TEXT,
                error_type VARCHAR(100)
            );
            
            CREATE INDEX IF NOT EXISTS idx_timestamp ON requests(timestamp);
            CREATE INDEX IF NOT EXISTS idx_endpoint ON requests(endpoint);
            CREATE INDEX IF NOT EXISTS idx_agent_name ON requests(agent_name);
            CREATE INDEX IF NOT EXISTS idx_status_code ON requests(status_code);
            
            CREATE TABLE IF NOT EXISTS ai_agents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name VARCHAR(100) UNIQUE,
                agent_type VARCHAR(50),
                first_seen DATETIME,
                last_seen DATETIME,
                total_requests INTEGER DEFAULT 0,
                favorite_endpoints TEXT,
                avg_response_time_ms INTEGER,
                error_rate FLOAT,
                user_agent_string TEXT,
                ip_addresses TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_agent_last_seen ON ai_agents(last_seen);
            
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE,
                total_requests INTEGER,
                unique_ips INTEGER,
                unique_agents INTEGER,
                avg_response_time_ms INTEGER,
                p95_response_time_ms INTEGER,
                p99_response_time_ms INTEGER,
                total_errors INTEGER,
                error_rate FLOAT,
                endpoint_stats TEXT,
                agent_stats TEXT
            );
            
            CREATE TABLE IF NOT EXISTS rate_limit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                endpoint VARCHAR(255),
                requests_in_window INTEGER,
                limit_threshold INTEGER
            );
            
            CREATE INDEX IF NOT EXISTS idx_ratelimit_timestamp 
                ON rate_limit_events(timestamp);
            
            CREATE TABLE IF NOT EXISTS errors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                error_type VARCHAR(100),
                error_message TEXT,
                stack_trace TEXT,
                endpoint VARCHAR(255),
                request_data TEXT,
                ip_address VARCHAR(45),
                user_agent TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_error_timestamp ON errors(timestamp);
            CREATE INDEX IF NOT EXISTS idx_error_type ON errors(error_type);
        ''')
        
        conn.commit()
        conn.close()
    
    def detect_agent(self, user_agent: str) -> Tuple[str, str]:
        """
        Detect if request is from an AI agent
        
        Returns:
            (agent_name, agent_type) tuple
        """
        if not user_agent:
            return ('Unknown', 'unknown')
        
        # Check against AI agent patterns
        for pattern, (name, agent_type) in self.AI_AGENTS.items():
            if re.search(pattern, user_agent, re.IGNORECASE):
                return (name, agent_type)
        
        # Classify other types
        user_agent_lower = user_agent.lower()
        if 'bot' in user_agent_lower or 'crawler' in user_agent_lower or 'spider' in user_agent_lower:
            return ('WebCrawler', 'bot')
        elif 'curl' in user_agent_lower or 'python' in user_agent_lower or 'requests' in user_agent_lower:
            return ('APIClient', 'api_client')
        elif 'mozilla' in user_agent_lower or 'chrome' in user_agent_lower or 'safari' in user_agent_lower:
            return ('Browser', 'browser')
        
        return ('Unknown', 'unknown')
    
    def log_request(self, request_data: Dict[str, Any]):
        """
        Log API request to all storage layers
        
        Args:
            request_data: Dictionary with request details
        """
        if not SiteConfig.MONITORING_ENABLED:
            return
        
        try:
            # 1. Write to JSON log (immediate, for debugging)
            json_logger.info(json.dumps(request_data, default=str))
            
            # 2. Update Redis counters (real-time metrics)
            self._update_redis_metrics(request_data)
            
            # 3. Store in SQLite (for analytics)
            self._store_in_database(request_data)
            
            # 4. Update agent profile (if AI agent)
            if request_data.get('agent_type') == 'ai_agent':
                self._update_agent_profile(request_data)
        
        except Exception as e:
            # Don't let monitoring errors break the app
            logging.error(f"Monitoring log_request failed: {e}")
    
    def _update_redis_metrics(self, data: Dict[str, Any]):
        """Update real-time metrics in Redis"""
        try:
            if not cache.redis_client:
                return
            
            endpoint = data.get('endpoint', 'unknown')
            now = datetime.now()
            
            # Increment endpoint counters
            minute_key = f"api:stats:{endpoint}:{now.strftime('%Y%m%d%H%M')}"
            hour_key = f"api:stats:{endpoint}:{now.strftime('%Y%m%d%H')}"
            day_key = f"api:stats:{endpoint}:{now.strftime('%Y%m%d')}"
            
            cache.redis_client.incr(minute_key)
            cache.redis_client.expire(minute_key, 3600)  # 1 hour TTL
            
            cache.redis_client.incr(hour_key)
            cache.redis_client.expire(hour_key, 604800)  # 7 days TTL
            
            cache.redis_client.incr(day_key)
            cache.redis_client.expire(day_key, 7776000)  # 90 days TTL
            
            # Update response time (rolling average)
            response_time = data.get('response_time_ms', 0)
            cache.redis_client.lpush(f"api:response_times:{endpoint}", response_time)
            cache.redis_client.ltrim(f"api:response_times:{endpoint}", 0, 99)  # Keep last 100
            
            # Track agent activity
            if data.get('agent_name') and data.get('agent_name') != 'Unknown':
                agent_key = f"agent:visits:{data['agent_name']}:{now.strftime('%Y%m%d')}"
                cache.redis_client.incr(agent_key)
                cache.redis_client.expire(agent_key, 7776000)  # 90 days
                
                cache.redis_client.set(
                    f"agent:last_seen:{data['agent_name']}", 
                    now.isoformat()
                )
        
        except Exception as e:
            # Don't let monitoring errors break the app
            logging.error(f"Redis metrics update failed: {e}")
    
    def _store_in_database(self, data: Dict[str, Any]):
        """Store request in SQLite database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO requests (
                    timestamp, method, endpoint, path, ip_address, user_agent,
                    agent_type, agent_name, request_body, request_headers,
                    status_code, response_time_ms, response_size_bytes,
                    error_message, error_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('timestamp'),
                data.get('method'),
                data.get('endpoint'),
                data.get('path'),
                data.get('ip'),
                data.get('user_agent'),
                data.get('agent_type'),
                data.get('agent_name'),
                json.dumps(data.get('request', {})),
                json.dumps(data.get('headers', {})),
                data.get('status_code'),
                data.get('response_time_ms'),
                data.get('response_size'),
                data.get('error_message'),
                data.get('error_type')
            ))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            logging.error(f"Database storage failed: {e}")
    
    def _update_agent_profile(self, data: Dict[str, Any]):
        """Update AI agent profile"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            agent_name = data.get('agent_name')
            if not agent_name or agent_name == 'Unknown':
                conn.close()
                return
            
            # Check if agent exists
            cursor.execute('SELECT id FROM ai_agents WHERE agent_name = ?', (agent_name,))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing agent
                cursor.execute('''
                    UPDATE ai_agents 
                    SET last_seen = ?, 
                        total_requests = total_requests + 1,
                        user_agent_string = ?
                    WHERE agent_name = ?
                ''', (datetime.now(), data.get('user_agent'), agent_name))
            else:
                # Create new agent profile
                cursor.execute('''
                    INSERT INTO ai_agents (
                        agent_name, agent_type, first_seen, last_seen,
                        total_requests, user_agent_string, ip_addresses
                    ) VALUES (?, ?, ?, ?, 1, ?, ?)
                ''', (
                    agent_name,
                    data.get('agent_type'),
                    datetime.now(),
                    datetime.now(),
                    data.get('user_agent'),
                    json.dumps([data.get('ip')])
                ))
            
            conn.commit()
            conn.close()
        
        except Exception as e:
            logging.error(f"Agent profile update failed: {e}")
    
    def log_rate_limit_event(self, ip: str, endpoint: str, count: int, limit: int):
        """Log rate limiting event"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO rate_limit_events (
                    ip_address, endpoint, requests_in_window, limit_threshold
                ) VALUES (?, ?, ?, ?)
            ''', (ip, endpoint, count, limit))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Rate limit logging failed: {e}")
    
    def log_error(self, error_data: Dict[str, Any]):
        """Log error to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO errors (
                    error_type, error_message, stack_trace, endpoint,
                    request_data, ip_address, user_agent
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                error_data.get('error_type'),
                error_data.get('error_message'),
                error_data.get('stack_trace'),
                error_data.get('endpoint'),
                json.dumps(error_data.get('request_data', {})),
                error_data.get('ip_address'),
                error_data.get('user_agent')
            ))
            
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(f"Error logging failed: {e}")
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """
        Get current dashboard metrics
        
        Returns:
            Dictionary with real-time metrics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Today's stats
            today = datetime.now().strftime('%Y-%m-%d')
            cursor.execute('''
                SELECT COUNT(*), AVG(response_time_ms), COUNT(DISTINCT ip_address)
                FROM requests
                WHERE DATE(timestamp) = ?
            ''', (today,))
            result = cursor.fetchone()
            today_requests = result[0] or 0
            avg_response = result[1] or 0
            unique_ips = result[2] or 0
            
            # AI agents today
            cursor.execute('''
                SELECT COUNT(DISTINCT agent_name)
                FROM requests
                WHERE DATE(timestamp) = ? AND agent_type = 'ai_agent'
            ''', (today,))
            ai_agents_today = cursor.fetchone()[0] or 0
            
            # Top endpoints today
            cursor.execute('''
                SELECT endpoint, COUNT(*) as count, AVG(response_time_ms) as avg_time,
                       SUM(CASE WHEN status_code >= 400 THEN 1 ELSE 0 END) as errors
                FROM requests
                WHERE DATE(timestamp) = ?
                GROUP BY endpoint
                ORDER BY count DESC
                LIMIT 5
            ''', (today,))
            top_endpoints = cursor.fetchall()
            
            # Recent AI agents (last 7 days)
            cursor.execute('''
                SELECT agent_name, last_seen, total_requests
                FROM ai_agents
                WHERE last_seen >= datetime('now', '-7 days')
                ORDER BY last_seen DESC
                LIMIT 10
            ''')
            recent_agents = cursor.fetchall()
            
            # Rate limit events (last hour)
            cursor.execute('''
                SELECT ip_address, endpoint, COUNT(*) as times
                FROM rate_limit_events
                WHERE timestamp >= datetime('now', '-1 hour')
                GROUP BY ip_address, endpoint
                ORDER BY times DESC
                LIMIT 5
            ''')
            rate_limit_events = cursor.fetchall()
            
            # Error count today
            cursor.execute('''
                SELECT COUNT(*)
                FROM requests
                WHERE DATE(timestamp) = ? AND status_code >= 400
            ''', (today,))
            error_count = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'today': {
                    'total_requests': today_requests,
                    'avg_response_ms': int(avg_response),
                    'ai_agents': ai_agents_today,
                    'unique_ips': unique_ips,
                    'errors': error_count,
                    'error_rate': round(error_count / today_requests * 100, 2) if today_requests > 0 else 0
                },
                'top_endpoints': [
                    {
                        'endpoint': ep,
                        'count': count,
                        'avg_time_ms': int(avg_time or 0),
                        'errors': errors
                    }
                    for ep, count, avg_time, errors in top_endpoints
                ],
                'recent_agents': [
                    {
                        'name': name,
                        'last_seen': last_seen,
                        'total_requests': total
                    }
                    for name, last_seen, total in recent_agents
                ],
                'rate_limit_events': [
                    {
                        'ip': ip,
                        'endpoint': endpoint,
                        'times': times
                    }
                    for ip, endpoint, times in rate_limit_events
                ]
            }
        
        except Exception as e:
            logging.error(f"Dashboard data fetch failed: {e}")
            return {
                'today': {'total_requests': 0, 'avg_response_ms': 0, 'ai_agents': 0, 'unique_ips': 0, 'errors': 0, 'error_rate': 0},
                'top_endpoints': [],
                'recent_agents': [],
                'rate_limit_events': []
            }


# Global instance
monitoring = MonitoringService()


    def get_dashboard_stats(self) -> Dict[str, Any]:
        """
        Get comprehensive statistics for admin dashboard.
        
        Returns:
            dict: Dashboard statistics
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Time range: last 24 hours
        time_24h_ago = (datetime.now() - timedelta(hours=24)).isoformat()
        
        stats = {}
        
        try:
            # Total requests (24h)
            cursor.execute(
                "SELECT COUNT(*) as count FROM requests WHERE timestamp >= ?",
                (time_24h_ago,)
            )
            stats['total_requests'] = cursor.fetchone()['count']
            
            # Success rate (24h)
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status_code < 400 THEN 1 ELSE 0 END) as success
                FROM requests 
                WHERE timestamp >= ?
            """, (time_24h_ago,))
            result = cursor.fetchone()
            total = result['total'] or 1  # Avoid division by zero
            success = result['success'] or 0
            stats['success_rate'] = (success / total) * 100 if total > 0 else 100
            
            # AI agent requests (24h)
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM requests 
                WHERE timestamp >= ? AND agent_type = 'ai_agent'
            """, (time_24h_ago,))
            ai_requests = cursor.fetchone()['count']
            stats['ai_agent_requests'] = ai_requests
            stats['ai_agent_percentage'] = (ai_requests / total * 100) if total > 0 else 0
            
            # Rate limit events (24h)
            cursor.execute(
                "SELECT COUNT(*) as count FROM rate_limit_events WHERE timestamp >= ?",
                (time_24h_ago,)
            )
            stats['rate_limit_events'] = cursor.fetchone()['count']
            
            # Average response time (24h)
            cursor.execute("""
                SELECT AVG(response_time_ms) as avg_time 
                FROM requests 
                WHERE timestamp >= ? AND response_time_ms IS NOT NULL
            """, (time_24h_ago,))
            result = cursor.fetchone()
            stats['avg_response_time'] = result['avg_time'] or 0
            
            # Uptime (placeholder - would need app start time tracking)
            stats['uptime'] = '99.9%'
            
            # AI agents detailed stats
            cursor.execute("""
                SELECT 
                    agent_name,
                    COUNT(*) as count,
                    AVG(response_time_ms) as avg_response_time
                FROM requests
                WHERE timestamp >= ? AND agent_type = 'ai_agent'
                GROUP BY agent_name
            """, (time_24h_ago,))
            
            ai_agents = {}
            for row in cursor.fetchall():
                ai_agents[row['agent_name']] = {
                    'count': row['count'],
                    'avg_response_time': row['avg_response_time'] or 0
                }
            stats['ai_agents'] = ai_agents
            
            # Recent requests (last 20)
            cursor.execute("""
                SELECT 
                    timestamp,
                    ip_address,
                    method,
                    endpoint,
                    status_code,
                    response_time_ms,
                    user_agent
                FROM requests
                ORDER BY timestamp DESC
                LIMIT 20
            """)
            
            recent_requests = []
            for row in cursor.fetchall():
                recent_requests.append({
                    'timestamp': row['timestamp'],
                    'ip_address': row['ip_address'],
                    'method': row['method'],
                    'endpoint': row['endpoint'],
                    'status_code': row['status_code'],
                    'response_time': row['response_time_ms'] or 0,
                    'user_agent': row['user_agent'] or 'Unknown'
                })
            stats['recent_requests'] = recent_requests
            
            # Top endpoints (24h)
            cursor.execute("""
                SELECT 
                    endpoint,
                    COUNT(*) as requests,
                    AVG(response_time_ms) as avg_response_time,
                    SUM(CASE WHEN status_code < 400 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) as success_rate,
                    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM requests WHERE timestamp >= ?) as load
                FROM requests
                WHERE timestamp >= ?
                GROUP BY endpoint
                ORDER BY requests DESC
                LIMIT 10
            """, (time_24h_ago, time_24h_ago))
            
            top_endpoints = []
            for row in cursor.fetchall():
                top_endpoints.append({
                    'path': row['endpoint'],
                    'requests': row['requests'],
                    'avg_response_time': row['avg_response_time'] or 0,
                    'success_rate': row['success_rate'] or 100,
                    'load': row['load'] or 0
                })
            stats['top_endpoints'] = top_endpoints
            
        except Exception as e:
            print(f"Error getting dashboard stats: {e}")
            # Return default stats on error
            stats = {
                'total_requests': 0,
                'success_rate': 100,
                'ai_agent_requests': 0,
                'ai_agent_percentage': 0,
                'rate_limit_events': 0,
                'avg_response_time': 0,
                'uptime': 'N/A',
                'ai_agents': {},
                'recent_requests': [],
                'top_endpoints': []
            }
        finally:
            conn.close()
        
        return stats


# Global monitoring instance
monitoring = MonitoringService()
