"""
Test environment variable loading
"""

import os
from dotenv import load_dotenv

print("\n=== Testing Environment Loading ===\n")

# Test 1: Before loading
print("1. Before load_dotenv():")
print(f"   OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT FOUND')[:30]}...")

# Test 2: Load from backend/.env
print("\n2. Loading backend/.env...")
load_dotenv('backend/.env')
print(f"   OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY', 'NOT FOUND')[:30]}...")

# Test 3: Check if it works in a module
print("\n3. Testing in module context...")
import sys
sys.path.insert(0, 'backend')

# This simulates what happens in the backend
api_key = os.getenv("OPENAI_API_KEY")
if api_key and api_key != "your_api_key_here":
    print(f"   ✅ API key found: {api_key[:30]}...")
    print(f"   Length: {len(api_key)}")
else:
    print("   ❌ API key not found or is placeholder")

print("\n" + "="*50 + "\n")
