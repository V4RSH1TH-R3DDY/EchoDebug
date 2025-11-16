import requests
import json

BASE_URL = "http://localhost:8000"

print("Testing EchoDebug API Endpoints\n" + "="*50)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
response = requests.get(f"{BASE_URL}/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

# Test 2: Intent parsing
print("\n2. Testing intent parsing...")
response = requests.post(f"{BASE_URL}/intent", json={
    "text": "find all syntax errors in main.py"
})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Code search
print("\n3. Testing code search...")
response = requests.post(f"{BASE_URL}/search", json={
    "query": "FastAPI",
    "lang": "python"
})
print(f"Status: {response.status_code}")
results = response.json()["results"]
print(f"Found {len(results)} results")
if results:
    print(f"First result: {results[0]['file']}:{results[0]['line']}")

# Test 4: Symbol search
print("\n4. Testing symbol search...")
response = requests.post(f"{BASE_URL}/symbols", json={
    "name": "parse_intent",
    "lang": "python"
})
print(f"Status: {response.status_code}")
symbols = response.json()["symbols"]
print(f"Found {len(symbols)} symbols")
if symbols:
    print(f"Symbol: {symbols[0]}")

# Test 5: Run command
print("\n5. Testing command execution...")
response = requests.post(f"{BASE_URL}/run", json={
    "cmd": "python --version"
})
print(f"Status: {response.status_code}")
result = response.json()
print(f"Exit code: {result['exit']}")
print(f"Output: {result['stdout'].strip()}")

# Test 6: Explain trace
print("\n6. Testing stack trace explanation...")
response = requests.post(f"{BASE_URL}/explain-trace", json={
    "trace": 'File "test.py", line 42\nZeroDivisionError: division by zero'
})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 7: Propose fix (placeholder)
print("\n7. Testing propose fix...")
response = requests.post(f"{BASE_URL}/propose-fix", json={
    "file": "test.py",
    "goal": "fix indentation"
})
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

print("\n" + "="*50)
print("All tests completed!")
