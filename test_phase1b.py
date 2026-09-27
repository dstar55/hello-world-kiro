#!/usr/bin/env python3
"""
Test script for Phase 1B endpoints (tokenize, detect-language, sentiment)
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:5000"

def print_result(test_name: str, response: requests.Response):
    """Pretty print test results"""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
        
        if data.get('success'):
            print(f"✅ SUCCESS - Processing time: {data.get('processing_time_ms', 'N/A')}ms")
        else:
            print(f"❌ FAILED - Error: {data.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Could not parse JSON: {e}")
        print(response.text)
    
    return response.status_code == 200

def test_tokenize():
    """Test tokenization endpoint"""
    tests = [
        {
            "name": "Tokenize with GPT-4",
            "payload": {
                "text": "Hello World! This is a test of the tokenization API.",
                "model": "gpt-4"
            }
        },
        {
            "name": "Tokenize with GPT-4o",
            "payload": {
                "text": "The quick brown fox jumps over the lazy dog. This is a longer text to count more tokens.",
                "model": "gpt-4o"
            }
        },
        {
            "name": "Tokenize with Claude",
            "payload": {
                "text": "Machine learning models need accurate token counting for cost estimation.",
                "model": "claude"
            }
        }
    ]
    
    print("\n" + "="*60)
    print("TOKENIZATION TESTS")
    print("="*60)
    
    passed = 0
    for test in tests:
        response = requests.post(
            f"{BASE_URL}/api/text/tokenize",
            json=test["payload"],
            headers={"Content-Type": "application/json"}
        )
        if print_result(test["name"], response):
            passed += 1
    
    return passed, len(tests)

def test_detect_language():
    """Test language detection endpoint"""
    tests = [
        {
            "name": "Detect English",
            "payload": {"text": "Hello, how are you today?"}
        },
        {
            "name": "Detect French",
            "payload": {"text": "Bonjour, comment allez-vous aujourd'hui?"}
        },
        {
            "name": "Detect Spanish",
            "payload": {"text": "Hola, ¿cómo estás hoy?"}
        },
        {
            "name": "Detect German",
            "payload": {"text": "Guten Tag, wie geht es Ihnen heute?"}
        },
        {
            "name": "Detect Japanese",
            "payload": {"text": "こんにちは、今日はお元気ですか？"}
        },
        {
            "name": "Detect Portuguese",
            "payload": {"text": "Olá, como você está hoje?"}
        }
    ]
    
    print("\n" + "="*60)
    print("LANGUAGE DETECTION TESTS")
    print("="*60)
    
    passed = 0
    for test in tests:
        response = requests.post(
            f"{BASE_URL}/api/text/detect-language",
            json=test["payload"],
            headers={"Content-Type": "application/json"}
        )
        if print_result(test["name"], response):
            passed += 1
    
    return passed, len(tests)

def test_sentiment():
    """Test sentiment analysis endpoint"""
    tests = [
        {
            "name": "Positive Sentiment",
            "payload": {"text": "I absolutely love this product! It's amazing and exceeded all my expectations!"}
        },
        {
            "name": "Negative Sentiment",
            "payload": {"text": "This is terrible. I hate it. Waste of money and time. Very disappointed."}
        },
        {
            "name": "Neutral Sentiment",
            "payload": {"text": "The product arrived on time. It is as described in the listing."}
        },
        {
            "name": "Mixed Sentiment",
            "payload": {"text": "The product has some good features but also some serious flaws. It's okay I guess."}
        },
        {
            "name": "Strong Positive",
            "payload": {"text": "Best purchase ever! Fantastic, brilliant, wonderful! Highly recommend! ⭐⭐⭐⭐⭐"}
        },
        {
            "name": "Strong Negative",
            "payload": {"text": "Worst experience ever. Horrible, awful, disgusting. Don't buy this garbage!"}
        }
    ]
    
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS TESTS")
    print("="*60)
    
    passed = 0
    for test in tests:
        response = requests.post(
            f"{BASE_URL}/api/text/sentiment",
            json=test["payload"],
            headers={"Content-Type": "application/json"}
        )
        if print_result(test["name"], response):
            passed += 1
    
    return passed, len(tests)

def test_caching():
    """Test that caching works for language detection and sentiment"""
    print("\n" + "="*60)
    print("CACHING TESTS")
    print("="*60)
    
    text = "This is a test for caching functionality"
    
    # First call - should not be cached
    print("\n--- First call (should NOT be cached) ---")
    response1 = requests.post(
        f"{BASE_URL}/api/text/detect-language",
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    data1 = response1.json()
    print(f"Cached: {data1.get('cached', False)}")
    print(f"Processing time: {data1.get('processing_time_ms')}ms")
    
    # Second call - should be cached
    print("\n--- Second call (SHOULD be cached) ---")
    response2 = requests.post(
        f"{BASE_URL}/api/text/detect-language",
        json={"text": text},
        headers={"Content-Type": "application/json"}
    )
    data2 = response2.json()
    print(f"Cached: {data2.get('cached', False)}")
    print(f"Processing time: {data2.get('processing_time_ms')}ms")
    
    if data1.get('cached') == False and data2.get('cached') == True:
        print("\n✅ Caching works correctly!")
        return 1, 1
    else:
        print("\n❌ Caching might not be working as expected")
        return 0, 1

def main():
    """Run all Phase 1B tests"""
    print("\n" + "🚀"*30)
    print("PHASE 1B ML ENDPOINTS TEST SUITE")
    print("🚀"*30)
    
    try:
        # Test health endpoint first
        print("\nChecking if server is running...")
        health = requests.get(f"{BASE_URL}/health", timeout=2)
        if health.status_code == 200:
            print("✅ Server is running!")
        else:
            print("⚠️ Server responded but might have issues")
    except Exception as e:
        print(f"❌ Cannot connect to server at {BASE_URL}")
        print(f"Error: {e}")
        print("\nPlease start the server with: python app.py")
        return
    
    # Run all tests
    results = []
    
    results.append(test_tokenize())
    results.append(test_detect_language())
    results.append(test_sentiment())
    results.append(test_caching())
    
    # Summary
    total_passed = sum(r[0] for r in results)
    total_tests = sum(r[1] for r in results)
    
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print("\n🎉 All tests passed! Phase 1B is fully functional!")
    else:
        print(f"\n⚠️ {total_tests - total_passed} test(s) failed. Please review the output above.")

if __name__ == "__main__":
    main()
