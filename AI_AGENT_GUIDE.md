# 🤖 AI Agent Developer Guide

**Complete guide for AI agents and developers integrating with {{ site_config.SITE_NAME }}**

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Discovery](#discovery)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
- [Batch Processing](#batch-processing)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Code Examples](#code-examples)

---

## 🚀 Quick Start

### Step 1: Discover the API

AI agents can discover this API through multiple channels:

```bash
# Primary discovery file for AI agents
curl https://kiro.fractus.io/llms.txt

# OpenAPI 3.0 specification
curl https://kiro.fractus.io/openapi.json

# Model Context Protocol card
curl https://kiro.fractus.io/.well-known/mcp.json

# Robots.txt with AI agent rules
curl https://kiro.fractus.io/robots.txt
```

### Step 2: Make Your First Request

```bash
curl https://kiro.fractus.io/api/text/uppercase \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'
```

### Step 3: Use Batch Processing

```bash
curl https://kiro.fractus.io/api/batch \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {"operation": "uppercase", "text": "hello"},
      {"operation": "reverse", "text": "world"}
    ]
  }'
```

---

## 🔍 Discovery

### Automatic Discovery

This API follows the `/llms.txt` standard for AI agent discovery:

**Discovery Flow:**
```
1. AI Agent checks robots.txt → Finds /llms.txt
2. AI Agent reads /llms.txt → Gets API description
3. AI Agent fetches /openapi.json → Gets full API spec
4. AI Agent starts using API → Success!
```

### Machine-Readable Files

| File | Purpose | Format |
|------|---------|--------|
| `/llms.txt` | Human-readable API description | Text |
| `/openapi.json` | Complete API specification | JSON (OpenAPI 3.0) |
| `/robots.txt` | Crawler rules and discovery | Text |
| `/.well-known/mcp.json` | Model Context Protocol card | JSON |
| `/sitemap.xml` | Site structure | XML |

---

## 🔐 Authentication

**No authentication required!** This is a public API designed for easy access.

Optional headers for tracking (not required):
```
X-Agent-Name: YourAgentName
X-Agent-Version: 1.0.0
```

---

## 📡 API Endpoints

### Base URL
```
https://kiro.fractus.io
```

### Text Operations

#### 1. Uppercase
Convert text to uppercase.

**Endpoint:** `POST /api/text/uppercase`

**Request:**
```json
{
  "text": "hello world"
}
```

**Response:**
```json
{
  "success": true,
  "result": "HELLO WORLD"
}
```

#### 2. Lowercase
Convert text to lowercase.

**Endpoint:** `POST /api/text/lowercase`

**Request:**
```json
{
  "text": "HELLO WORLD"
}
```

**Response:**
```json
{
  "success": true,
  "result": "hello world"
}
```

#### 3. Reverse
Reverse the text.

**Endpoint:** `POST /api/text/reverse`

**Request:**
```json
{
  "text": "hello"
}
```

**Response:**
```json
{
  "success": true,
  "result": "olleh"
}
```

#### 4. Length
Get text length.

**Endpoint:** `POST /api/text/length`

**Request:**
```json
{
  "text": "hello"
}
```

**Response:**
```json
{
  "success": true,
  "result": 5
}
```

#### 5. Word Count
Count words in text.

**Endpoint:** `POST /api/text/word-count`

**Request:**
```json
{
  "text": "hello world"
}
```

**Response:**
```json
{
  "success": true,
  "result": 2
}
```

### List Operations

**Endpoint:** `GET /api/operations`

Get list of all available operations with examples.

**Response:**
```json
{
  "success": true,
  "operations": [
    {
      "name": "uppercase",
      "description": "Convert text to uppercase",
      "example": {"text": "hello", "result": "HELLO"}
    }
  ],
  "count": 10,
  "batch_endpoint": "https://kiro.fractus.io/api/batch",
  "max_batch_size": 100
}
```

---

## 📦 Batch Processing

Process multiple operations in a single HTTP request for improved efficiency.

### Benefits
- ✅ Reduce HTTP overhead
- ✅ Faster processing (single request vs multiple)
- ✅ Consistent results
- ✅ Lower network latency

### Endpoint
**POST /api/batch**

### Request Format
```json
{
  "operations": [
    {"operation": "uppercase", "text": "hello"},
    {"operation": "reverse", "text": "world"},
    {"operation": "length", "text": "test"}
  ]
}
```

### Response Format
```json
{
  "success": true,
  "results": [
    {"success": true, "result": "HELLO", "operation": "uppercase"},
    {"success": true, "result": "dlrow", "operation": "reverse"},
    {"success": true, "result": 4, "operation": "length"}
  ],
  "processed": 3,
  "failed": 0,
  "total": 3,
  "elapsed_ms": 5.234
}
```

### Limitations
- Maximum **100 operations** per request
- Each operation is validated independently
- Failed operations don't affect others

### Example: Batch Processing
```python
import requests

response = requests.post(
    "https://kiro.fractus.io/api/batch",
    json={
        "operations": [
            {"operation": "uppercase", "text": "hello"},
            {"operation": "lowercase", "text": "WORLD"},
            {"operation": "reverse", "text": "AI"},
            {"operation": "length", "text": "testing"}
        ]
    }
)

data = response.json()
print(f"Processed: {data['processed']}/{data['total']}")
for result in data['results']:
    print(f"{result['operation']}: {result['result']}")
```

---

## ⏱️ Rate Limiting

To ensure fair usage, we implement rate limiting:

### Standard Limits
- **100 requests per minute**
- **1,000 requests per hour**

### AI Agent Limits (Higher)
Detected AI agents get higher limits:
- **200 requests per minute**
- Agents: GPTBot, Claude-Web, PerplexityBot, Googlebot-AI, Meta-AI, AppleBot-AI

### Identification
Set your User-Agent to be recognized:
```
User-Agent: GPTBot/1.0
User-Agent: Claude-Web/1.0
```

### Rate Limit Headers
Every response includes rate limit information:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

### Handling Rate Limits
When rate limited, you'll receive:

**Status:** `429 Too Many Requests`

**Response:**
```json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
```

**Best Practice:**
```python
import requests
import time

def call_api_with_retry(url, data):
    response = requests.post(url, json=data)
    
    if response.status_code == 429:
        retry_after = response.json().get('retry_after', 60)
        print(f"Rate limited. Waiting {retry_after} seconds...")
        time.sleep(retry_after)
        return call_api_with_retry(url, data)
    
    return response.json()
```

---

## ⚠️ Error Handling

### HTTP Status Codes

| Status | Meaning | Action |
|--------|---------|--------|
| 200 | Success | Parse response |
| 400 | Bad Request | Check request format |
| 429 | Too Many Requests | Wait and retry |
| 500 | Server Error | Retry later |

### Error Response Format
```json
{
  "success": false,
  "error": "Description of what went wrong",
  "example": {
    "text": "correct format"
  }
}
```

### Example: Robust Error Handling
```python
import requests

def safe_api_call(operation, text):
    try:
        response = requests.post(
            f"https://kiro.fractus.io/api/text/{operation}",
            json={"text": text},
            timeout=10
        )
        
        # Check HTTP status
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print("Rate limited!")
            return None
        else:
            print(f"Error: {response.status_code}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Use it
result = safe_api_call("uppercase", "hello")
if result:
    print(result['result'])
```

---

## ✨ Best Practices

### 1. Use Batch Processing
When making multiple requests, always use `/api/batch`:

❌ **Bad:**
```python
# Multiple HTTP requests (slow)
for text in texts:
    requests.post("/api/text/uppercase", json={"text": text})
```

✅ **Good:**
```python
# Single batch request (fast)
operations = [{"operation": "uppercase", "text": t} for t in texts]
requests.post("/api/batch", json={"operations": operations})
```

### 2. Respect Rate Limits
- Check `X-RateLimit-Remaining` header
- Implement exponential backoff
- Use batch processing to reduce request count

### 3. Handle Errors Gracefully
- Validate input before sending
- Implement retry logic
- Log errors for debugging

### 4. Set User-Agent
Help us identify your agent:
```python
headers = {
    "User-Agent": "MyAgent/1.0",
    "X-Agent-Name": "MyAgent",
    "X-Agent-Version": "1.0.0"
}
```

### 5. Cache Results
For repetitive operations, implement local caching:
```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_uppercase(text):
    response = requests.post(
        "https://kiro.fractus.io/api/text/uppercase",
        json={"text": text}
    )
    return response.json()['result']
```

---

## 💻 Code Examples

### Python (requests)
```python
import requests

# Single operation
def uppercase(text):
    response = requests.post(
        "https://kiro.fractus.io/api/text/uppercase",
        json={"text": text}
    )
    return response.json()['result']

# Batch operations
def batch_process(operations):
    response = requests.post(
        "https://kiro.fractus.io/api/batch",
        json={"operations": operations}
    )
    return response.json()

# Usage
print(uppercase("hello"))  # HELLO

results = batch_process([
    {"operation": "uppercase", "text": "hello"},
    {"operation": "reverse", "text": "world"}
])
print(results)
```

### JavaScript (fetch)
```javascript
// Single operation
async function uppercase(text) {
  const response = await fetch('https://kiro.fractus.io/api/text/uppercase', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: text})
  });
  const data = await response.json();
  return data.result;
}

// Batch operations
async function batchProcess(operations) {
  const response = await fetch('https://kiro.fractus.io/api/batch', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({operations: operations})
  });
  return await response.json();
}

// Usage
const result = await uppercase('hello');
console.log(result);  // HELLO

const results = await batchProcess([
  {operation: 'uppercase', text: 'hello'},
  {operation: 'reverse', text: 'world'}
]);
console.log(results);
```

### cURL
```bash
# Single operation
curl -X POST https://kiro.fractus.io/api/text/uppercase \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world"}'

# Batch operations
curl -X POST https://kiro.fractus.io/api/batch \
  -H "Content-Type: application/json" \
  -d '{
    "operations": [
      {"operation": "uppercase", "text": "hello"},
      {"operation": "reverse", "text": "world"}
    ]
  }'
```

### Go
```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "net/http"
)

type TextRequest struct {
    Text string `json:"text"`
}

type TextResponse struct {
    Success bool   `json:"success"`
    Result  string `json:"result"`
}

func uppercase(text string) (string, error) {
    req := TextRequest{Text: text}
    body, _ := json.Marshal(req)
    
    resp, err := http.Post(
        "https://kiro.fractus.io/api/text/uppercase",
        "application/json",
        bytes.NewBuffer(body),
    )
    if err != nil {
        return "", err
    }
    defer resp.Body.Close()
    
    var result TextResponse
    json.NewDecoder(resp.Body).Decode(&result)
    return result.Result, nil
}

func main() {
    result, _ := uppercase("hello")
    fmt.Println(result)  // HELLO
}
```

---

## 📚 Additional Resources

### Documentation
- **Interactive Docs:** https://kiro.fractus.io/api/docs
- **OpenAPI Spec:** https://kiro.fractus.io/openapi.json
- **llms.txt:** https://kiro.fractus.io/llms.txt

### Testing
- **API Test Page:** https://kiro.fractus.io/api-test
- **Health Check:** https://kiro.fractus.io/health

### Monitoring
- **API Status:** https://kiro.fractus.io/health
- **Capabilities:** https://kiro.fractus.io/api/capabilities

### Support
- **GitHub:** https://github.com/dstar55/hello-world-kiro
- **Issues:** https://github.com/dstar55/hello-world-kiro/issues

---

## 🎯 Summary

This API is designed to be:
- ✅ **Easy to discover** - Following /llms.txt standard
- ✅ **Simple to use** - No authentication, clear docs
- ✅ **Efficient** - Batch processing support
- ✅ **Reliable** - Rate limiting and error handling
- ✅ **Well-documented** - Multiple formats (OpenAPI, llms.txt, HTML)

**Get started now:** https://kiro.fractus.io/api/docs

---

*Last updated: 2026-10-02 | API Version: 1.2.0*
