# Text Transformation API Documentation

## Base URL
```
http://localhost:5000/api/text
```

## Authentication
No authentication required for Phase 1.

---

## Endpoints

### Group A: Instant Operations (< 10ms)

#### 1. Base64 Encode
**POST** `/api/text/base64/encode`

Encode text to Base64 format.

**Request:**
```json
{
  "text": "Hello World"
}
```

**Response:**
```json
{
  "success": true,
  "text": "Hello World",
  "encoded": "SGVsbG8gV29ybGQ=",
  "processing_time_ms": 1
}
```

---

#### 2. Base64 Decode
**POST** `/api/text/base64/decode`

Decode Base64 to plain text.

**Request:**
```json
{
  "encoded": "SGVsbG8gV29ybGQ="
}
```

**Response:**
```json
{
  "success": true,
  "encoded": "SGVsbG8gV29ybGQ=",
  "text": "Hello World",
  "processing_time_ms": 1
}
```

---

#### 3. Hash Text
**POST** `/api/text/hash`

Generate cryptographic hashes for text.

**Request:**
```json
{
  "text": "Hello World",
  "algorithms": ["sha256", "md5"]  // optional, defaults to all
}
```

**Response:**
```json
{
  "success": true,
  "text": "Hello World",
  "hashes": {
    "sha256": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
    "md5": "b10a8db164e0754105b7a99be72e3fe5"
  },
  "processing_time_ms": 2
}
```

**Available algorithms:** `md5`, `sha1`, `sha256`, `sha512`

---

#### 4. Normalize Text
**POST** `/api/text/normalize`

Clean and normalize text with various options.

**Request:**
```json
{
  "text": "  Hello   World!  ",
  "options": {
    "lowercase": false,
    "remove_extra_spaces": true,
    "remove_punctuation": false,
    "remove_numbers": false,
    "strip": true
  }
}
```

**Response:**
```json
{
  "success": true,
  "original": "  Hello   World!  ",
  "normalized": "Hello World!",
  "processing_time_ms": 1
}
```

**Options (all optional):**
- `lowercase` (boolean): Convert to lowercase
- `remove_extra_spaces` (boolean): Remove extra whitespace (default: true)
- `remove_punctuation` (boolean): Remove punctuation
- `remove_numbers` (boolean): Remove numbers
- `strip` (boolean): Strip leading/trailing whitespace (default: true)

---

#### 5. Text Statistics
**POST** `/api/text/stats`

Get comprehensive text statistics.

**Request:**
```json
{
  "text": "Hello World. This is a test."
}
```

**Response:**
```json
{
  "success": true,
  "text": "Hello World. This is a test.",
  "stats": {
    "characters": 28,
    "characters_no_spaces": 23,
    "words": 6,
    "sentences": 2,
    "paragraphs": 1,
    "unique_words": 6,
    "average_word_length": 3.83,
    "reading_time_seconds": 1.44,
    "speaking_time_seconds": 2.4
  },
  "processing_time_ms": 3
}
```

---

#### 6. Extract Entities
**POST** `/api/text/extract`

Extract URLs, emails, and phone numbers from text.

**Request:**
```json
{
  "text": "Contact me at john@example.com or visit https://example.com. Call 555-123-4567",
  "extract_types": ["urls", "emails", "phones"]  // optional, defaults to all
}
```

**Response:**
```json
{
  "success": true,
  "text": "Contact me at john@example.com...",
  "extracted": {
    "urls": ["https://example.com"],
    "emails": ["john@example.com"],
    "phones": ["555-123-4567"]
  },
  "processing_time_ms": 5
}
```

**Available extract types:** `urls`, `emails`, `phones`, `all`

---

#### 7. Case Conversion
**POST** `/api/text/case-convert`

Convert text to various case formats.

**Request:**
```json
{
  "text": "hello world example",
  "case_type": "camel"
}
```

**Response:**
```json
{
  "success": true,
  "original": "hello world example",
  "converted": "helloWorldExample",
  "case_type": "camel",
  "processing_time_ms": 1
}
```

**Available case types:**
- `upper` - UPPERCASE
- `lower` - lowercase
- `title` - Title Case
- `sentence` - Sentence case
- `camel` - camelCase
- `pascal` - PascalCase
- `snake` - snake_case
- `kebab` - kebab-case

---

### Group B: Lightweight ML (Phase 1B - Placeholders)

#### 8. Tokenize
**POST** `/api/text/tokenize`

Count tokens for LLM models.

**Status:** Placeholder (Phase 1B implementation pending)

**Request:**
```json
{
  "text": "Hello World",
  "model": "gpt-4"  // gpt-3.5-turbo, gpt-4, claude, etc.
}
```

**Current Response:**
```json
{
  "success": true,
  "text": "Hello World",
  "model": "gpt-4",
  "token_count": 2,
  "estimated_cost_usd": 0.0,
  "processing_time_ms": 15,
  "note": "Placeholder implementation - Phase 1B will use proper tokenizers"
}
```

---

#### 9. Detect Language
**POST** `/api/text/detect-language`

Detect the language of text.

**Status:** Placeholder (Phase 1B implementation pending)

**Request:**
```json
{
  "text": "Bonjour le monde"
}
```

**Current Response:**
```json
{
  "success": true,
  "text": "Bonjour le monde",
  "language": {
    "code": "en",
    "name": "English",
    "confidence": 1.0,
    "note": "Placeholder implementation - Phase 1B will use language detection library"
  },
  "processing_time_ms": 25,
  "cached": false
}
```

---

#### 10. Sentiment Analysis
**POST** `/api/text/sentiment`

Analyze sentiment of text.

**Status:** Placeholder (Phase 1B implementation pending)

**Request:**
```json
{
  "text": "I love this product!"
}
```

**Current Response:**
```json
{
  "success": true,
  "text": "I love this product!",
  "sentiment": "neutral",
  "scores": {
    "positive": 0.0,
    "negative": 0.0,
    "neutral": 1.0,
    "compound": 0.0
  },
  "processing_time_ms": 12,
  "cached": false,
  "note": "Placeholder implementation - Phase 1B will use VADER sentiment analysis"
}
```

---

### System Endpoints

#### Health Check
**GET** `/health`

Check system health and Redis connection status.

**Response:**
```json
{
  "status": "healthy",
  "redis": "connected",
  "cache_stats": {
    "enabled": true,
    "memory_used_mb": 2.5,
    "total_keys": 150
  },
  "timestamp": "2024-09-27T10:30:00",
  "version": "1.1.0"
}
```

---

#### API Information
**GET** `/api`

Get API documentation and available endpoints.

**Response:**
```json
{
  "name": "Hello World API",
  "version": "1.1.0",
  "endpoints": {
    "text_api": {
      "base_url": "/api/text",
      "documentation": "Text transformation and analysis endpoints",
      "available_operations": [
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
    "currency_api": {
      "base_url": "/api/convert",
      "documentation": "Currency conversion with live rates"
    },
    "health_check": {
      "base_url": "/health",
      "documentation": "System health status"
    }
  }
}
```

---

## Error Responses

All endpoints return consistent error format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `400` - Bad Request (missing required fields, invalid input)
- `500` - Internal Server Error
- `501` - Not Implemented (Phase 1B/2 endpoints)

---

## Response Format

All successful responses include:
- `success`: Boolean indicating success
- `processing_time_ms`: Processing time in milliseconds
- Endpoint-specific data fields

Cached responses include:
- `cached`: Boolean indicating if result was from cache

---

## Caching

Endpoints with caching enabled:
- `/detect-language` - 1 hour TTL
- `/sentiment` - 30 minutes TTL
- (More in Phase 2 with embeddings)

Cache is Redis-based with automatic fallback if Redis is unavailable.

---

## Example Usage

### cURL Examples

**Base64 Encode:**
```bash
curl -X POST http://localhost:5000/api/text/base64/encode \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World"}'
```

**Hash Text:**
```bash
curl -X POST http://localhost:5000/api/text/hash \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World", "algorithms": ["sha256", "md5"]}'
```

**Text Statistics:**
```bash
curl -X POST http://localhost:5000/api/text/stats \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World. This is a test."}'
```

**Health Check:**
```bash
curl http://localhost:5000/health
```

### Python Examples

```python
import requests

# Base64 Encode
response = requests.post('http://localhost:5000/api/text/base64/encode', 
    json={'text': 'Hello World'})
print(response.json())

# Hash Text
response = requests.post('http://localhost:5000/api/text/hash',
    json={'text': 'Hello World', 'algorithms': ['sha256', 'md5']})
print(response.json())

# Text Statistics
response = requests.post('http://localhost:5000/api/text/stats',
    json={'text': 'Hello World. This is a test.'})
print(response.json())
```

---

## Development Roadmap

### ✅ Phase 1A (Current)
- Infrastructure setup with Redis
- 7 instant text operations
- Health checks and monitoring
- API documentation

### 🔄 Phase 1B (Next)
- Proper tokenization (tiktoken)
- Language detection (langdetect/fasttext)
- Sentiment analysis (VADER)

### 📅 Phase 1C (Future)
- Text embeddings (sentence-transformers)
- Text similarity
- Batch processing

### 📅 Phase 2 (Future)
- Named Entity Recognition (spaCy)
- Text classification
- PII detection
- Cloud provider integration

---

## Running Locally

### With Docker Compose

```bash
# Start services
docker-compose up -d

# Check logs
docker-compose logs -f app

# Stop services
docker-compose down
```

### Without Docker

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis (separate terminal)
redis-server

# Set environment variables
export REDIS_URL=redis://localhost:6379/0

# Run application
python app.py
```

Visit: http://localhost:5000

---

## Notes

- All text processing is UTF-8 compatible
- Maximum recommended text length: 10,000 characters for instant operations
- Redis caching is optional - API works without it (just slower)
- All timestamps are in ISO 8601 format
- Processing times are approximate and may vary
