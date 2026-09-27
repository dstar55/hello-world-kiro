"""
Text API Routes

RESTful API endpoints for text transformations and analysis.
All endpoints are under /api/text/
"""

from flask import Blueprint, request, jsonify
from services.text_service import TextService
from services.cache_service import cache
import time

# Create blueprint
text_bp = Blueprint('text', __name__, url_prefix='/api/text')

# Initialize service
text_service = TextService()


# ============================================================================
# Helper Functions
# ============================================================================

def get_processing_time(start_time):
    """Calculate processing time in milliseconds"""
    return int((time.time() - start_time) * 1000)


def create_error_response(error_message, status_code=400):
    """Create standardized error response"""
    return jsonify({
        'success': False,
        'error': str(error_message)
    }), status_code


# ============================================================================
# Group A: Encoding/Decoding
# ============================================================================

@text_bp.route('/base64/encode', methods=['POST'])
def base64_encode():
    """
    Encode text to Base64
    
    Request:
        POST /api/text/base64/encode
        {
            "text": "Hello World"
        }
    
    Response:
        {
            "success": true,
            "text": "Hello World",
            "encoded": "SGVsbG8gV29ybGQ=",
            "processing_time_ms": 1
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        start_time = time.time()
        
        encoded = text_service.base64_encode(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'encoded': encoded,
            'processing_time_ms': get_processing_time(start_time)
        })
    except Exception as e:
        return create_error_response(str(e))


@text_bp.route('/base64/decode', methods=['POST'])
def base64_decode():
    """
    Decode Base64 to text
    
    Request:
        POST /api/text/base64/decode
        {
            "encoded": "SGVsbG8gV29ybGQ="
        }
    
    Response:
        {
            "success": true,
            "encoded": "SGVsbG8gV29ybGQ=",
            "text": "Hello World",
            "processing_time_ms": 1
        }
    """
    try:
        data = request.get_json()
        if not data or 'encoded' not in data:
            return create_error_response('Missing required field: encoded')
        
        encoded = data.get('encoded', '')
        start_time = time.time()
        
        text = text_service.base64_decode(encoded)
        
        return jsonify({
            'success': True,
            'encoded': encoded,
            'text': text,
            'processing_time_ms': get_processing_time(start_time)
        })
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group A: Hashing
# ============================================================================

@text_bp.route('/hash', methods=['POST'])
def hash_text():
    """
    Generate cryptographic hashes for text
    
    Request:
        POST /api/text/hash
        {
            "text": "Hello World",
            "algorithms": ["sha256", "md5"]  // optional, defaults to all
        }
    
    Response:
        {
            "success": true,
            "text": "Hello World",
            "hashes": {
                "sha256": "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e",
                "md5": "b10a8db164e0754105b7a99be72e3fe5"
            },
            "processing_time_ms": 2
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        algorithms = data.get('algorithms', ['md5', 'sha1', 'sha256', 'sha512'])
        start_time = time.time()
        
        hashes = text_service.hash_text(text, algorithms)
        
        return jsonify({
            'success': True,
            'text': text,
            'hashes': hashes,
            'processing_time_ms': get_processing_time(start_time)
        })
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group A: Text Normalization
# ============================================================================

@text_bp.route('/normalize', methods=['POST'])
def normalize():
    """
    Normalize text with various cleaning options
    
    Request:
        POST /api/text/normalize
        {
            "text": "  Hello   World!  ",
            "options": {
                "lowercase": false,
                "remove_extra_spaces": true,
                "remove_punctuation": false,
                "strip": true
            }
        }
    
    Response:
        {
            "success": true,
            "original": "  Hello   World!  ",
            "normalized": "Hello World!",
            "processing_time_ms": 1
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        options = data.get('options', {})
        start_time = time.time()
        
        normalized = text_service.normalize(text, options)
        
        return jsonify({
            'success': True,
            'original': text,
            'normalized': normalized,
            'processing_time_ms': get_processing_time(start_time)
        })
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group A: Text Statistics
# ============================================================================

@text_bp.route('/stats', methods=['POST'])
def text_stats():
    """
    Get comprehensive text statistics
    
    Request:
        POST /api/text/stats
        {
            "text": "Hello World. This is a test."
        }
    
    Response:
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
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        start_time = time.time()
        
        stats = text_service.get_stats(text)
        
        return jsonify({
            'success': True,
            'text': text,
            'stats': stats,
            'processing_time_ms': get_processing_time(start_time)
        })
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group A: Extraction
# ============================================================================

@text_bp.route('/extract', methods=['POST'])
def extract():
    """
    Extract URLs, emails, and phone numbers from text
    
    Request:
        POST /api/text/extract
        {
            "text": "Contact me at john@example.com or visit https://example.com",
            "extract_types": ["urls", "emails"]  // optional, defaults to all
        }
    
    Response:
        {
            "success": true,
            "text": "Contact me at...",
            "extracted": {
                "urls": ["https://example.com"],
                "emails": ["john@example.com"]
            },
            "processing_time_ms": 5
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        extract_types = data.get('extract_types', None)
        start_time = time.time()
        
        extracted = text_service.extract(text, extract_types)
        
        return jsonify({
            'success': True,
            'text': text,
            'extracted': extracted,
            'processing_time_ms': get_processing_time(start_time)
        })
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group A: Case Conversion
# ============================================================================

@text_bp.route('/case-convert', methods=['POST'])
def case_convert():
    """
    Convert text to various case formats
    
    Request:
        POST /api/text/case-convert
        {
            "text": "hello world",
            "case_type": "camel"  // upper, lower, title, sentence, camel, pascal, snake, kebab
        }
    
    Response:
        {
            "success": true,
            "original": "hello world",
            "converted": "helloWorld",
            "case_type": "camel",
            "processing_time_ms": 1
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data or 'case_type' not in data:
            return create_error_response('Missing required fields: text, case_type')
        
        text = data.get('text', '')
        case_type = data.get('case_type', '')
        start_time = time.time()
        
        converted = text_service.convert_case(text, case_type)
        
        return jsonify({
            'success': True,
            'original': text,
            'converted': converted,
            'case_type': case_type,
            'processing_time_ms': get_processing_time(start_time)
        })
    except ValueError as e:
        return create_error_response(str(e))
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group B: Lightweight ML (Phase 1B - Placeholders)
# ============================================================================

@text_bp.route('/tokenize', methods=['POST'])
def tokenize():
    """
    Count tokens for LLM models using tiktoken
    
    Request:
        POST /api/text/tokenize
        {
            "text": "Hello World",
            "model": "gpt-4"  // gpt-4, gpt-4o, gpt-3.5-turbo, claude, etc.
        }
    
    Response:
        {
            "success": true,
            "text": "Hello World",
            "model": "gpt-4",
            "encoding": "cl100k_base",
            "token_count": 2,
            "estimated_cost_usd": 0.00006,
            "processing_time_ms": 15
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        model = data.get('model', 'gpt-4')
        start_time = time.time()
        
        result = text_service.tokenize(text, model)
        result['processing_time_ms'] = get_processing_time(start_time)
        result['success'] = True
        
        return jsonify(result)
    except Exception as e:
        return create_error_response(str(e))


@text_bp.route('/detect-language', methods=['POST'])
def detect_language():
    """
    Detect language of text using langdetect
    
    Request:
        POST /api/text/detect-language
        {
            "text": "Bonjour le monde"
        }
    
    Response:
        {
            "success": true,
            "text": "Bonjour le monde",
            "language": {
                "code": "fr",
                "name": "French",
                "confidence": 0.9999,
                "alternatives": [...]  // included if confidence < 0.95
            },
            "processing_time_ms": 25,
            "cached": false
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        start_time = time.time()
        
        # Check cache first
        cache_key = f"lang:{hash(text)}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            cached_result['cached'] = True
            cached_result['processing_time_ms'] = get_processing_time(start_time)
            return jsonify(cached_result)
        
        # Detect language
        result = text_service.detect_language(text)
        
        response = {
            'success': True,
            'text': text,
            'language': result,
            'processing_time_ms': get_processing_time(start_time),
            'cached': False
        }
        
        # Cache for 1 hour
        cache.set(cache_key, response, ttl=3600)
        
        return jsonify(response)
    except Exception as e:
        return create_error_response(str(e))


@text_bp.route('/sentiment', methods=['POST'])
def sentiment():
    """
    Analyze sentiment of text using VADER
    
    Request:
        POST /api/text/sentiment
        {
            "text": "I love this product!"
        }
    
    Response:
        {
            "success": true,
            "text": "I love this product!",
            "sentiment": "positive",
            "scores": {
                "positive": 0.75,
                "negative": 0.0,
                "neutral": 0.25,
                "compound": 0.6369
            },
            "processing_time_ms": 12,
            "cached": false
        }
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return create_error_response('Missing required field: text')
        
        text = data.get('text', '')
        start_time = time.time()
        
        # Check cache first
        cache_key = f"sentiment:{hash(text)}"
        cached_result = cache.get(cache_key)
        
        if cached_result:
            cached_result['cached'] = True
            cached_result['processing_time_ms'] = get_processing_time(start_time)
            return jsonify(cached_result)
        
        # Analyze sentiment
        result = text_service.analyze_sentiment(text)
        
        response = {
            'success': True,
            'text': text,
            'sentiment': result['sentiment'],
            'scores': result['scores'],
            'processing_time_ms': get_processing_time(start_time),
            'cached': False
        }
        
        # Cache for 30 minutes
        cache.set(cache_key, response, ttl=1800)
        
        return jsonify(response)
    except Exception as e:
        return create_error_response(str(e))


# ============================================================================
# Group C: Embeddings (Phase 2 - Not Implemented Yet)
# ============================================================================

@text_bp.route('/embeddings', methods=['POST'])
def embeddings():
    """
    Generate text embeddings
    
    NOTE: Phase 2 implementation
    """
    return jsonify({
        'success': False,
        'error': 'Embeddings endpoint not yet implemented (Phase 2)'
    }), 501


@text_bp.route('/similarity', methods=['POST'])
def similarity():
    """
    Compare similarity between two texts
    
    NOTE: Phase 2 implementation
    """
    return jsonify({
        'success': False,
        'error': 'Similarity endpoint not yet implemented (Phase 2)'
    }), 501
