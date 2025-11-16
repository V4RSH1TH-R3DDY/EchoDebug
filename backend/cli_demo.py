#!/usr/bin/env python3
"""
EchoDebug CLI Demo
Test the full pipeline without VS Code extension
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from modules.ai_reasoning import parse_intent
from modules.intent_router import get_router, register_handlers
from modules.code_index import get_index, rebuild_index
from modules.linter import find_errors
from modules.code_parser import find_symbols, search_code

def print_banner():
    print("\n" + "="*60)
    print("  🎙️  EchoDebug CLI Demo")
    print("  Voice-Controlled AI Debugger")
    print("="*60 + "\n")

def print_section(title):
    print(f"\n{'─'*60}")
    print(f"  {title}")
    print('─'*60)

def demo_intent_parsing():
    """Demo intent parsing"""
    print_section("1. Intent Parsing")
    
    commands = [
        "find all syntax errors in main.py",
        "explain what the parse_intent function does",
        "where is FastAPI imported",
        "run tests"
    ]
    
    for cmd in commands:
        print(f"\n💬 Command: '{cmd}'")
        intent = parse_intent(cmd)
        print(f"   Intent: {intent['intent']}")
        print(f"   Confidence: {intent['confidence']}")
        if intent['entities'].get('file'):
            print(f"   File: {intent['entities']['file']}")
        if intent['entities'].get('symbol'):
            print(f"   Symbol: {intent['entities']['symbol']}")

def demo_code_indexing():
    """Demo code indexing"""
    print_section("2. Code Indexing")
    
    print("\n📚 Building code index...")
    stats = rebuild_index(force=True)
    print(f"   ✓ Indexed {stats['files_indexed']} files")
    print(f"   ✓ Found {stats['symbols_found']} symbols")
    print(f"   ✓ Completed in {stats['duration_seconds']:.2f}s")

def demo_symbol_search():
    """Demo symbol search"""
    print_section("3. Symbol Search")
    
    symbols = ["parse_intent", "FastAPI", "IntentType"]
    
    for symbol in symbols:
        print(f"\n🔍 Searching for: '{symbol}'")
        results = find_symbols(symbol, "python")
        
        if results:
            print(f"   Found {len(results)} location(s):")
            for r in results[:3]:  # Show first 3
                print(f"   • {r['kind']} in {r['file']}:{r['line']}")
                if r.get('signature'):
                    print(f"     {r['signature']}")
        else:
            print(f"   Not found")

def demo_error_detection():
    """Demo error detection"""
    print_section("4. Error Detection")
    
    # Create a test file with errors
    test_file = "test_errors.py"
    with open(test_file, 'w') as f:
        f.write("""
def broken_function()
    x = 1
    y = 2
    return x + z  # z is not defined
    
class MyClass
    def __init__(self):
        pass
""")
    
    print(f"\n🔍 Checking '{test_file}' for errors...")
    result = find_errors(test_file, "python")
    
    if result['errors']:
        print(f"\n   ❌ Found {result['total_errors']} error(s):")
        for err in result['errors'][:5]:
            print(f"   • Line {err['line']}: {err['message']}")
    
    if result['warnings']:
        print(f"\n   ⚠️  Found {result['total_warnings']} warning(s):")
        for warn in result['warnings'][:3]:
            print(f"   • Line {warn['line']}: {warn['message']}")
    
    # Clean up
    os.remove(test_file)

def demo_intent_routing():
    """Demo intent routing"""
    print_section("5. Intent Routing")
    
    # Register handlers
    register_handlers()
    router = get_router()
    
    print("\n🎯 Testing intent routing...")
    
    # Test find_symbol intent
    intent = parse_intent("find where parse_intent is defined")
    print(f"\n💬 Command: 'find where parse_intent is defined'")
    print(f"   Intent: {intent['intent']}")
    
    from modules.intent_schema import validate_intent
    intent_obj = validate_intent(intent)
    result = router.route(intent_obj)
    
    print(f"   Status: {result['status']}")
    if result.get('result'):
        symbols = result['result']
        if isinstance(symbols, list) and symbols:
            print(f"   Found {len(symbols)} location(s)")
            print(f"   First: {symbols[0].get('file')}:{symbols[0].get('line')}")

def demo_code_search():
    """Demo code search"""
    print_section("6. Code Search")
    
    queries = ["FastAPI", "def ", "import"]
    
    for query in queries:
        print(f"\n🔍 Searching for: '{query}'")
        results = search_code(query, "python")
        
        if results:
            print(f"   Found {len(results)} match(es)")
            # Show first match
            first = results[0]
            print(f"   First: {first['file']}:{first['line']}")
            print(f"   Preview: {first['preview'][:60]}...")

def main():
    """Run all demos"""
    print_banner()
    
    # Check if OpenAI API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key and api_key != "your_api_key_here":
        print("✓ OpenAI API key detected - Using GPT-4 for intent parsing")
    else:
        print("⚠️  No OpenAI API key - Using keyword-based intent parsing")
        print("   Set OPENAI_API_KEY in .env to enable GPT-4\n")
    
    try:
        demo_intent_parsing()
        demo_code_indexing()
        demo_symbol_search()
        demo_error_detection()
        demo_intent_routing()
        demo_code_search()
        
        print("\n" + "="*60)
        print("  ✅ All demos completed successfully!")
        print("="*60 + "\n")
        
        print("Next steps:")
        print("  1. Add OPENAI_API_KEY to backend/.env for GPT-4 integration")
        print("  2. Start the API server: python backend/main.py")
        print("  3. Test with: python test_phase2_3.py")
        print("  4. Build VS Code extension for full experience\n")
    
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
