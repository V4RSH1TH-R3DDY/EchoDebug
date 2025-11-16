"""
Test script for Phase 2 (Intent Schema & Router) and Phase 3 (Code Indexing)
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_intent_schema():
    """Test Phase 2: Intent Schema & Router"""
    print_section("PHASE 2: Intent Schema & Router")
    
    # Test various natural language commands
    test_commands = [
        "find all syntax errors in main.py",
        "explain what the parse_intent function does",
        "where is userData modified",
        "run tests for this file",
        "fix the indentation in code_parser.py",
        "format main.py",
        "rename counter to item_count"
    ]
    
    print("\n1. Testing Intent Classification:")
    for cmd in test_commands:
        response = requests.post(f"{BASE_URL}/intent", json={"text": cmd})
        if response.status_code == 200:
            intent = response.json()
            print(f"\n   Command: '{cmd}'")
            print(f"   Intent: {intent['intent']} (confidence: {intent['confidence']})")
            print(f"   Entities: {json.dumps(intent['entities'], indent=6)}")
        else:
            print(f"   ERROR: {response.status_code}")
    
    print("\n2. Testing Intent Router:")
    # Test routing with a simple command
    response = requests.post(f"{BASE_URL}/intent/route", json={
        "text": "find where parse_intent is defined"
    })
    
    if response.status_code == 200:
        result = response.json()
        print(f"   Status: {result.get('status')}")
        print(f"   Intent: {result.get('intent')}")
        if result.get('result'):
            print(f"   Result: {json.dumps(result['result'][:2], indent=6)}...")  # First 2 results
    else:
        print(f"   ERROR: {response.status_code}")

def test_code_indexing():
    """Test Phase 3: Symbol Indexing & Code Intelligence"""
    print_section("PHASE 3: Code Indexing & Intelligence")
    
    print("\n1. Building Code Index:")
    response = requests.post(f"{BASE_URL}/index/build", params={"force": True})
    if response.status_code == 200:
        result = response.json()
        stats = result.get('stats', {})
        print(f"   Files indexed: {stats.get('files_indexed')}")
        print(f"   Symbols found: {stats.get('symbols_found')}")
        print(f"   Files skipped: {stats.get('files_skipped')}")
        print(f"   Duration: {stats.get('duration_seconds', 0):.2f}s")
    else:
        print(f"   ERROR: {response.status_code}")
    
    # Wait a moment for index to complete
    time.sleep(1)
    
    print("\n2. Index Statistics:")
    response = requests.get(f"{BASE_URL}/index/stats")
    if response.status_code == 200:
        stats = response.json()
        print(f"   Total symbols: {stats.get('total_symbols')}")
        print(f"   Unique symbols: {stats.get('unique_symbols')}")
        print(f"   Files indexed: {stats.get('files_indexed')}")
        print(f"   Last indexed: {stats.get('last_indexed')}")
    else:
        print(f"   ERROR: {response.status_code}")
    
    print("\n3. Fast Symbol Search (using index):")
    test_symbols = ["parse_intent", "FastAPI", "search_code"]
    
    for symbol in test_symbols:
        response = requests.post(f"{BASE_URL}/symbols", json={
            "name": symbol,
            "lang": "python"
        })
        if response.status_code == 200:
            result = response.json()
            symbols = result.get('symbols', [])
            print(f"\n   Symbol: '{symbol}'")
            print(f"   Found: {len(symbols)} location(s)")
            if symbols:
                first = symbols[0]
                print(f"   First: {first.get('kind')} in {first.get('file')}:{first.get('line')}")
                if first.get('signature'):
                    print(f"   Signature: {first.get('signature')}")
        else:
            print(f"   ERROR: {response.status_code}")
    
    print("\n4. File Symbol Listing:")
    response = requests.get(f"{BASE_URL}/symbols/file/main.py")
    if response.status_code == 200:
        result = response.json()
        symbols = result.get('symbols', [])
        print(f"   File: main.py")
        print(f"   Symbols defined: {len(symbols)}")
        
        # Group by kind
        by_kind = {}
        for sym in symbols:
            kind = sym.get('kind', 'unknown')
            by_kind[kind] = by_kind.get(kind, 0) + 1
        
        for kind, count in by_kind.items():
            print(f"     - {kind}: {count}")
    else:
        print(f"   ERROR: {response.status_code}")

def test_performance():
    """Test performance improvements"""
    print_section("Performance Comparison")
    
    print("\n1. Symbol Search Speed:")
    
    # Test with index
    start = time.time()
    response = requests.post(f"{BASE_URL}/symbols", json={
        "name": "parse_intent",
        "lang": "python"
    })
    indexed_time = time.time() - start
    
    print(f"   With index: {indexed_time*1000:.2f}ms")
    
    # Test with search
    start = time.time()
    response = requests.post(f"{BASE_URL}/search", json={
        "query": "parse_intent",
        "lang": "python"
    })
    search_time = time.time() - start
    
    print(f"   With search: {search_time*1000:.2f}ms")
    print(f"   Speedup: {search_time/indexed_time:.1f}x faster")

def test_intent_validation():
    """Test intent validation and error handling"""
    print_section("Intent Validation & Error Handling")
    
    print("\n1. Testing Invalid Intent:")
    # This should still work but with lower confidence
    response = requests.post(f"{BASE_URL}/intent", json={
        "text": "make me a sandwich"
    })
    if response.status_code == 200:
        intent = response.json()
        print(f"   Command: 'make me a sandwich'")
        print(f"   Intent: {intent['intent']} (confidence: {intent['confidence']})")
        print(f"   Note: Falls back to default intent")
    
    print("\n2. Testing Destructive Intent (should require confirmation):")
    response = requests.post(f"{BASE_URL}/intent/route", json={
        "text": "delete all my code"
    })
    if response.status_code == 200:
        result = response.json()
        print(f"   Status: {result.get('status')}")
        if result.get('status') == 'confirmation_required':
            print(f"   ✓ Correctly requires confirmation for destructive action")

def main():
    print("\n" + "="*60)
    print("  EchoDebug Phase 2 & 3 Testing")
    print("  Testing Intent Schema, Router, and Code Indexing")
    print("="*60)
    
    try:
        # Check if server is running
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("\n❌ Server not running! Start with: python backend/main.py")
            return
        
        # Run tests
        test_intent_schema()
        test_code_indexing()
        test_performance()
        test_intent_validation()
        
        print("\n" + "="*60)
        print("  ✓ All Phase 2 & 3 Tests Completed!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server!")
        print("   Start the backend with: python backend/main.py")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
