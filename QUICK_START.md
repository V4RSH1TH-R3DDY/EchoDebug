# 🚀 EchoDebug Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure (Optional)
```bash
cp .env.example .env
# Edit .env and add OPENAI_API_KEY for GPT-4 features
```

### 3. Start Server
```bash
python main.py
```
✓ Server running at http://localhost:8000

### 4. Test It
```bash
# Run CLI demo
python cli_demo.py

# Or test API
python test_complete.py
```

### 5. Explore API
Open http://localhost:8000/docs in your browser

---

## Quick Examples

### Find Errors in a File
```bash
curl -X POST http://localhost:8000/lint \
  -H "Content-Type: application/json" \
  -d '{"file": "main.py", "lang": "python"}'
```

### Parse Voice Command
```bash
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"text": "find where userData is modified"}'
```

### Search for Symbol
```bash
curl -X POST http://localhost:8000/symbols \
  -H "Content-Type: application/json" \
  -d '{"name": "FastAPI", "lang": "python"}'
```

### Build Code Index
```bash
curl -X POST http://localhost:8000/index/build?force=true
```

---

## Key Commands

| Command | Description |
|---------|-------------|
| `python main.py` | Start API server |
| `python cli_demo.py` | Run interactive demo |
| `python test_complete.py` | Run all tests |
| Visit `/docs` | Interactive API documentation |

---

## Features at a Glance

✅ **Intent Parsing** - Understands natural language commands
✅ **Code Indexing** - Fast symbol search (0.06s for 495 symbols)
✅ **Error Detection** - Pylint + Mypy + syntax checking
✅ **AI Fixes** - GPT-4 powered code repairs
✅ **Symbol Search** - Find functions, classes, variables
✅ **Code Search** - Pattern matching across files
✅ **Stack Traces** - Intelligent error analysis

---

## Common Use Cases

### 1. Find All Errors
```python
import requests
r = requests.post("http://localhost:8000/lint", 
                  json={"file": "app.py", "lang": "python"})
print(f"Errors: {r.json()['total_errors']}")
```

### 2. Search Code
```python
r = requests.post("http://localhost:8000/search",
                  json={"query": "def ", "lang": "python"})
print(f"Found {len(r.json()['results'])} matches")
```

### 3. Get Fix Suggestion
```python
r = requests.post("http://localhost:8000/propose-fix",
                  json={"file": "broken.py", "goal": "fix syntax"})
print(r.json()['rationale'])
```

---

## Troubleshooting

**Server won't start?**
- Check if port 8000 is available
- Install dependencies: `pip install -r requirements.txt`

**No OpenAI features?**
- Add `OPENAI_API_KEY` to `.env` file
- Features work without it (keyword-based fallback)

**Linting not working?**
- Install pylint: `pip install pylint`
- Install mypy: `pip install mypy`

**Index not building?**
- Check file permissions
- Run with `force=true` parameter

---

## Next Steps

1. ✅ **Test the API** - Run `python test_complete.py`
2. 🔑 **Add API Key** - Enable GPT-4 features
3. 🎨 **Build Frontend** - VS Code extension or web UI
4. 🚀 **Deploy** - Production server setup
5. 📱 **Extend** - Add more languages, features

---

## Need Help?

- 📖 Read `README.md` for full overview
- 📚 Check `IMPLEMENTATION_COMPLETE.md` for details
- 🔍 Visit `/docs` for API reference
- 🧪 Run `cli_demo.py` for examples

---

**You're ready to debug with your voice!** 🎙️
