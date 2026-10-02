"""
Batch Processing Routes for AI Agents

Provides efficient batch processing capabilities allowing AI agents to:
- Process multiple text operations in a single request
- Reduce HTTP overhead
- Get consistent results
"""

from flask import Blueprint, request, jsonify
from services.text_service import TextService
from config.site_config import SiteConfig
import time

batch_bp = Blueprint('batch', __name__)
text_service = TextService()

@batch_bp.route('/api/batch', methods=['POST'])
def batch_process():
    """
    Process multiple text operations in a single request.
    
    Request Body:
    {
        "operations": [
            {"operation": "uppercase", "text": "hello"},
            {"operation": "reverse", "text": "world"},
            {"operation": "length", "text": "test"}
        ]
    }
    
    Response:
    {
        "success": true,
        "results": [
            {"success": true, "result": "HELLO", "operation": "uppercase"},
            {"success": true, "result": "dlrow", "operation": "reverse"},
            {"success": true, "result": 4, "operation": "length"}
        ],
        "processed": 3,
        "failed": 0,
        "elapsed_ms": 5.234
    }
    """
    start_time = time.time()
    
    try:
        data = request.get_json()
        
        if not data or 'operations' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'operations' array in request body",
                "example": {
                    "operations": [
                        {"operation": "uppercase", "text": "hello"}
                    ]
                }
            }), 400
        
        operations = data['operations']
        
        if not isinstance(operations, list):
            return jsonify({
                "success": False,
                "error": "'operations' must be an array"
            }), 400
        
        if len(operations) == 0:
            return jsonify({
                "success": False,
                "error": "At least one operation is required"
            }), 400
        
        # Limit batch size to prevent abuse
        max_batch_size = 100
        if len(operations) > max_batch_size:
            return jsonify({
                "success": False,
                "error": f"Batch size exceeds maximum of {max_batch_size} operations",
                "received": len(operations)
            }), 400
        
        results = []
        processed = 0
        failed = 0
        
        for idx, op in enumerate(operations):
            try:
                # Validate operation structure
                if not isinstance(op, dict):
                    results.append({
                        "success": False,
                        "error": f"Operation at index {idx} is not an object",
                        "operation": None
                    })
                    failed += 1
                    continue
                
                operation = op.get('operation')
                text = op.get('text')
                
                if not operation:
                    results.append({
                        "success": False,
                        "error": "Missing 'operation' field",
                        "operation": None
                    })
                    failed += 1
                    continue
                
                if text is None:
                    results.append({
                        "success": False,
                        "error": "Missing 'text' field",
                        "operation": operation
                    })
                    failed += 1
                    continue
                
                # Process the operation
                result = process_operation(operation, str(text))
                
                if result['success']:
                    results.append({
                        "success": True,
                        "result": result['result'],
                        "operation": operation
                    })
                    processed += 1
                else:
                    results.append({
                        "success": False,
                        "error": result['error'],
                        "operation": operation
                    })
                    failed += 1
                    
            except Exception as e:
                results.append({
                    "success": False,
                    "error": str(e),
                    "operation": op.get('operation') if isinstance(op, dict) else None
                })
                failed += 1
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        return jsonify({
            "success": True,
            "results": results,
            "processed": processed,
            "failed": failed,
            "total": len(operations),
            "elapsed_ms": round(elapsed_ms, 3)
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def process_operation(operation: str, text: str) -> dict:
    """
    Process a single text operation.
    
    Returns:
        dict: {"success": bool, "result": any, "error": str}
    """
    try:
        operation = operation.lower().strip()
        
        # Map operations to service methods
        operations_map = {
            'uppercase': lambda t: t.upper(),
            'lowercase': lambda t: t.lower(),
            'reverse': lambda t: t[::-1],
            'length': lambda t: len(t),
            'word_count': lambda t: len(t.split()),
            'capitalize': lambda t: t.capitalize(),
            'title': lambda t: t.title(),
            'strip': lambda t: t.strip(),
            'swapcase': lambda t: t.swapcase(),
            'count_vowels': lambda t: sum(1 for c in t.lower() if c in 'aeiou')
        }
        
        if operation not in operations_map:
            return {
                "success": False,
                "error": f"Unknown operation: '{operation}'",
                "available_operations": list(operations_map.keys())
            }
        
        result = operations_map[operation](text)
        
        return {
            "success": True,
            "result": result
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@batch_bp.route('/api/operations', methods=['GET'])
def list_operations():
    """
    List all available text operations.
    
    Response:
    {
        "operations": [...],
        "count": 10
    }
    """
    operations = [
        {
            "name": "uppercase",
            "description": "Convert text to uppercase",
            "example": {"text": "hello", "result": "HELLO"}
        },
        {
            "name": "lowercase",
            "description": "Convert text to lowercase",
            "example": {"text": "HELLO", "result": "hello"}
        },
        {
            "name": "reverse",
            "description": "Reverse the text",
            "example": {"text": "hello", "result": "olleh"}
        },
        {
            "name": "length",
            "description": "Get text length",
            "example": {"text": "hello", "result": 5}
        },
        {
            "name": "word_count",
            "description": "Count words in text",
            "example": {"text": "hello world", "result": 2}
        },
        {
            "name": "capitalize",
            "description": "Capitalize first letter",
            "example": {"text": "hello", "result": "Hello"}
        },
        {
            "name": "title",
            "description": "Convert to title case",
            "example": {"text": "hello world", "result": "Hello World"}
        },
        {
            "name": "strip",
            "description": "Remove leading/trailing whitespace",
            "example": {"text": "  hello  ", "result": "hello"}
        },
        {
            "name": "swapcase",
            "description": "Swap uppercase/lowercase",
            "example": {"text": "Hello", "result": "hELLO"}
        },
        {
            "name": "count_vowels",
            "description": "Count vowels in text",
            "example": {"text": "hello", "result": 2}
        }
    ]
    
    return jsonify({
        "success": True,
        "operations": operations,
        "count": len(operations),
        "batch_endpoint": f"{SiteConfig.SITE_URL}/api/batch",
        "max_batch_size": 100
    }), 200
