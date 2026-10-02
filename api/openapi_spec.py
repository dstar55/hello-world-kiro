"""
OpenAPI 3.0 Specification Generator

Dynamically generates OpenAPI specification for the Text API.
Uses SiteConfig for all site-specific information.
"""

from flask import Blueprint, jsonify
from config import SiteConfig

openapi_bp = Blueprint('openapi', __name__)


def generate_openapi_spec():
    """
    Generate complete OpenAPI 3.0 specification.
    
    Returns:
        dict: OpenAPI 3.0 compliant specification
    """
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": SiteConfig.SITE_NAME,
            "description": SiteConfig.SITE_DESCRIPTION,
            "version": SiteConfig.API_VERSION,
            "contact": {
                "name": SiteConfig.ORG_NAME,
                "url": SiteConfig.ORG_URL,
                "email": SiteConfig.SUPPORT_EMAIL
            },
            "license": {
                "name": "MIT",
                "url": f"{SiteConfig.GITHUB_REPO}/blob/main/LICENSE"
            },
            "termsOfService": f"{SiteConfig.SITE_URL}/terms"
        },
        "servers": [
            {
                "url": SiteConfig.SITE_URL,
                "description": "Production server"
            }
        ],
        "tags": [
            {
                "name": "Text Processing",
                "description": "Text transformation and analysis operations"
            },
            {
                "name": "Currency",
                "description": "Currency conversion with live rates"
            },
            {
                "name": "System",
                "description": "Health checks and system information"
            }
        ],
        "paths": {
            "/api/text/base64/encode": {
                "post": {
                    "tags": ["Text Processing"],
                    "summary": "Encode text to Base64",
                    "description": "Convert plain text to Base64 encoding",
                    "operationId": "base64Encode",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["text"],
                                    "properties": {
                                        "text": {
                                            "type": "string",
                                            "description": "Text to encode",
                                            "example": "Hello World"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful encoding",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Base64EncodeResponse"
                                    }
                                }
                            }
                        },
                        "400": {
                            "$ref": "#/components/responses/BadRequest"
                        }
                    }
                }
            },
            "/api/text/base64/decode": {
                "post": {
                    "tags": ["Text Processing"],
                    "summary": "Decode Base64 to text",
                    "description": "Convert Base64 encoding to plain text",
                    "operationId": "base64Decode",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["encoded"],
                                    "properties": {
                                        "encoded": {
                                            "type": "string",
                                            "description": "Base64 encoded text",
                                            "example": "SGVsbG8gV29ybGQ="
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful decoding",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Base64DecodeResponse"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/text/hash": {
                "post": {
                    "tags": ["Text Processing"],
                    "summary": "Generate cryptographic hashes",
                    "description": "Generate MD5, SHA1, SHA256, and SHA512 hashes",
                    "operationId": "hashText",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["text"],
                                    "properties": {
                                        "text": {
                                            "type": "string",
                                            "description": "Text to hash"
                                        },
                                        "algorithms": {
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "enum": ["md5", "sha1", "sha256", "sha512"]
                                            },
                                            "description": "Hash algorithms to use (defaults to all)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Successful hashing"
                        }
                    }
                }
            },
            "/api/text/tokenize": {
                "post": {
                    "tags": ["Text Processing"],
                    "summary": "Count tokens for LLM models",
                    "description": "Calculate token count for GPT-4, GPT-3.5, Claude models",
                    "operationId": "tokenize",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["text"],
                                    "properties": {
                                        "text": {
                                            "type": "string",
                                            "description": "Text to tokenize"
                                        },
                                        "model": {
                                            "type": "string",
                                            "enum": ["gpt-4", "gpt-4o", "gpt-3.5-turbo", "claude"],
                                            "default": "gpt-4",
                                            "description": "Model to use for tokenization"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Token count calculated"
                        }
                    }
                }
            },
            "/api/convert": {
                "post": {
                    "tags": ["Currency"],
                    "summary": "Convert currency",
                    "description": "Convert between currencies with live exchange rates",
                    "operationId": "convertCurrency",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["amount", "from_currency", "to_currency"],
                                    "properties": {
                                        "amount": {
                                            "type": "number",
                                            "description": "Amount to convert"
                                        },
                                        "from_currency": {
                                            "type": "string",
                                            "enum": ["USD", "EUR", "GBP", "TRY", "RUB"],
                                            "description": "Source currency"
                                        },
                                        "to_currency": {
                                            "type": "string",
                                            "enum": ["USD", "EUR", "GBP", "TRY", "RUB"],
                                            "description": "Target currency"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Conversion successful"
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "tags": ["System"],
                    "summary": "Health check",
                    "description": "Check system health and Redis connection",
                    "operationId": "healthCheck",
                    "responses": {
                        "200": {
                            "description": "System healthy"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Base64EncodeResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "text": {"type": "string"},
                        "encoded": {"type": "string"},
                        "processing_time_ms": {"type": "integer"}
                    }
                },
                "Base64DecodeResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "encoded": {"type": "string"},
                        "text": {"type": "string"},
                        "processing_time_ms": {"type": "integer"}
                    }
                },
                "ErrorResponse": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "error": {"type": "string"}
                    }
                }
            },
            "responses": {
                "BadRequest": {
                    "description": "Bad request - missing required fields",
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ErrorResponse"
                            }
                        }
                    }
                }
            }
        }
    }
    
    return spec


@openapi_bp.route('/openapi.json')
def openapi_json():
    """
    Serve OpenAPI 3.0 specification as JSON.
    
    Returns:
        JSON response with complete OpenAPI spec
    """
    spec = generate_openapi_spec()
    return jsonify(spec)
