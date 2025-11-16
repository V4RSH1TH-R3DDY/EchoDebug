# 🚀 How to Use EchoDebug

## Step 1: Setup (One-Time)

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Configure (Optional - for AI features)
1. Open `backend/.env`
2. Replace `your_api_key_here` with your OpenAI API key
3. Get a key from: https://platform.openai.com/api-keys

**Note:** EchoDebug works without an API key (uses keyword-based parsing), but AI features require it.

---

## Step 2: Start the Server

```bash
# From the project root
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Server is now running!

---

## Step 3: Test It

### Option A: Run the CLI Demo (Recommended)
```bash
python backend/cli_demo.py
```

This will show you:
- Intent parsing examples
- Code indexing in action
- Symbol search
- Error detection
- Full pipeline demo

### Option B: Run Tests
```bash
python test_complete.py
```

### Option C: Use the API Directly

Open your browser: **http://localhost:8000/docs**

You'll see interactive API documentation where you can test all endpoints!

---

## Step 4: Try Some Commands

### Example 1: Find Errors in a File

**Using curl:**
```bash
curl -X POST http://localhost:8000/lint \
  -H "Content-Type: application/json" \
  -d "{\"file\": \"backend/main.py\", \"lang\": \"python\"}"
```

**Using Python:**
```python
import requests

response = requests.post("http://localhost:8000/lint", json={
    "file": "backend/main.py",
    "lang": "python"
})

result = response.json()
print(f"Found {result['total_errors']} errors")
print(f"Found {result['total_warnings']} warnings")
```

### Example 2: Parse a Voice Command

```python
import requests

response = requests.post("http://localhost:8000/intent", json={
    "text": "find all syntax errors in main.py"
})

intent = response.json()
print(f"Intent: {intent['intent']}")
print(f"File: {intent['entities']['file']}")
```

### Example 3: Search for a Symbol

```python
import requests

response = requests.post("http://localhost:8000/symbols", json={
    "name": "FastAPI",
    "lang": "python"
})

symbols = response.json()['symbols']
for sym in symbols:
    print(f"{sym['kind']} in {sym['file']}:{sym['line']}")
```

### Example 4: Build Code Index

```bash
curl -X POST http://localhost:8000/index/build?force=true
```

### Example 5: Get Fix Suggestion

```python
import requests

response = requests.post("http://localhost:8000/propose-fix", json={
    "file": "broken.py",
    "goal": "fix syntax error"
})

fix = response.json()
print(f"Rationale: {fix['rationale']}")
print(f"Risk: {fix['risk_level']}")
```

---

## Step 5: Explore the API

Visit **http://localhost:8000/docs** to see all available endpoints:

### Core Endpoints:
- `POST /stt` - Convert speech to text
- `POST /intent` - Parse natural language command
- `POST /intent/route` - Parse and execute in one call

### Code Analysis:
- `POST /search` - Search code by pattern
- `POST /symbols` - Find symbol definitions
- `POST /lint` - Find errors and warnings
- `POST /propose-fix` - Get AI-powered fix

### Indexing:
- `POST /index/build` - Build code index
- `GET /index/stats` - Get index statistics

### Execution:
- `POST /run` - Execute shell commands

---

## Common Use Cases

### Use Case 1: Check a File for Errors

```python
import requests

# Check for errors
response = requests.post("http://localhost:8000/lint", json={
    "file": "mycode.py",
    "lang": "python"
})

errors = response.json()

if errors['total_errors'] > 0:
    print("❌ Errors found:")
    for err in errors['errors']:
        print(f"  Line {err['line']}: {err['message']}")
else:
    print("✅ No errors!")
```

### Use Case 2: Find Where a Variable is Used

```python
import requests

# Search for symbol
response = requests.post("http://localhost:8000/symbols", json={
    "name": "userData",
    "lang": "python"
})

locations = response.json()['symbols']
print(f"Found {len(locations)} uses of 'userData':")
for loc in locations:
    print(f"  {loc['file']}:{loc['line']} ({loc['kind']})")
```

### Use Case 3: Natural Language Debugging

```python
import requests

# Parse what you want to do
response = requests.post("http://localhost:8000/intent/route", json={
    "text": "find where parse_intent is defined"
})

result = response.json()
if result['status'] == 'success':
    symbols = result['result']
    print(f"Found {len(symbols)} locations")
```

---

## Tips & Tricks

### 1. Build Index First
For faster searches, build the code index:
```bash
curl -X POST http://localhost:8000/index/build
```

### 2. Check Index Stats
See what's indexed:
```bash
curl http://localhost:8000/index/stats
```

### 3. Use Interactive Docs
The easiest way to test: http://localhost:8000/docs
- Click any endpoint
- Click "Try it out"
- Fill in parameters
- Click "Execute"

### 4. Enable AI Features
Add your OpenAI API key to `backend/.env`:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Then restart the server for:
- ✅ GPT-4 intent parsing (95%+ accuracy)
- ✅ Whisper speech-to-text
- ✅ AI-powered fix generation

### 5. Run in Background
```bash
# Windows
start python backend/main.py

# Linux/Mac
python backend/main.py &
```

---

## Troubleshooting

### Server won't start?
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Or use a different port
# Edit backend/.env and change PORT=8000 to PORT=8001
```

### Import errors?
```bash
# Make sure you're in the right directory
cd backend
pip install -r requirements.txt
```

### No OpenAI features?
- Check `backend/.env` has your API key
- Restart the server after adding the key
- Verify key at: https://platform.openai.com/api-keys

### Linting not working?
```bash
# Install linters
pip install pylint mypy
```

---

## What You Can Do

### Without API Key (Free):
✅ Parse intents (keyword-based)  
✅ Index and search code  
✅ Find symbols  
✅ Detect errors (pylint/mypy)  
✅ Search patterns  
✅ Execute commands  

### With API Key (Premium):
✅ GPT-4 intent parsing  
✅ Whisper speech-to-text  
✅ AI-powered fixes  
✅ Smart code explanations  
✅ Context-aware suggestions  

---

## Next Steps

1. ✅ **Start the server** - `python backend/main.py`
2. ✅ **Run the demo** - `python backend/cli_demo.py`
3. ✅ **Try the API** - Visit http://localhost:8000/docs
4. ✅ **Add API key** - Enable AI features
5. ✅ **Build something** - Integrate into your workflow

---

## Quick Reference

```bash
# Start server
python backend/main.py

# Run demo
python backend/cli_demo.py

# Run tests
python test_complete.py

# API docs
http://localhost:8000/docs

# Check status
curl http://localhost:8000/

# Build index
curl -X POST http://localhost:8000/index/build

# Find errors
curl -X POST http://localhost:8000/lint \
  -H "Content-Type: application/json" \
  -d '{"file": "main.py"}'
```

---

## Need Help?

- 📖 Read `README.md` for overview
- 📚 Check `QUICK_START.md` for setup
- 🔍 Visit `/docs` for API reference
- 🧪 Run `cli_demo.py` for examples
- 📝 See `FINAL_STATUS.md` for complete status

---

**You're ready to debug with AI!** 🎙️✨
