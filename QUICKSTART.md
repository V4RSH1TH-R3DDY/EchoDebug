# EchoDebug - Quick Start Guide

Get EchoDebug running in 5 minutes!

## Prerequisites

- Python 3.13+ installed
- Node.js 18+ installed
- VS Code installed

## Step 1: Start Backend (2 minutes)

```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is running!

## Step 2: Install Extension (2 minutes)

```bash
# Navigate to extension
cd vscode-extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile
```

✅ Extension is compiled!

## Step 3: Launch Extension (1 minute)

1. Open `vscode-extension` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. A new VS Code window opens

✅ Extension is loaded!

## Step 4: Test It! (1 minute)

In the new VS Code window:

1. Open any Python project (or the EchoDebug project itself)
2. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)
3. Enter: `find symbol FastAPI`
4. See results and navigate!

✅ It works!

## What You Can Do Now

### Find Symbols
```
Ctrl+Shift+V → "find symbol parse_intent"
```
Shows all locations, navigate to any

### Search Code
```
Ctrl+Shift+V → "find all errors in main.py"
```
Searches for patterns

### Explain Code
```
Select code → Ctrl+Shift+P → "EchoDebug: Explain Selection"
```
Gets explanation (placeholder for now)

### Build Index
```
Ctrl+Shift+P → "EchoDebug: Build Code Index"
```
Indexes your codebase for fast search

## Status Bar

Look for 🎤 icon in bottom-right:
- **Normal**: Backend connected
- **Red**: Backend not running
- **Yellow**: Processing command

## Configuration

Settings → Search "echodebug":
- Backend URL (default: http://localhost:8000)
- Highlight color
- Voice feedback (future)

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.13+

# Try installing dependencies again
pip install --upgrade -r requirements.txt
```

### Extension won't load
```bash
# Recompile
npm run compile

# Check for errors
npm run lint
```

### No results found
```bash
# Build index first
Ctrl+Shift+P → "EchoDebug: Build Code Index"
```

## Next Steps

### Add AI Intelligence (Optional)

1. Get OpenAI API key from https://platform.openai.com
2. Create `backend/.env`:
```bash
OPENAI_API_KEY=your_key_here
```
3. Restart backend
4. Intent parsing now uses GPT-4!

### Try More Commands

- "where is userData modified"
- "explain what this function does"
- "run tests"
- "find all syntax errors"

### Explore Features

- Check the webview panel (Ctrl+Shift+P → "EchoDebug: Show Panel")
- Try different highlight colors in settings
- Use keyboard shortcut (Ctrl+Shift+V)

## Development Mode

### Watch Mode (Auto-compile)
```bash
cd vscode-extension
npm run watch
```

### Backend Hot Reload
```bash
cd backend
uvicorn main:app --reload
```

### Debug Extension
1. Set breakpoints in TypeScript files
2. Press F5
3. Use Debug Console

## Documentation

- `README.md` - Project overview
- `PHASE4_SUMMARY.md` - Extension details
- `test_extension.md` - Testing guide
- `PROJECT_STATUS.md` - Complete status

## Support

Check the logs:
- **Backend**: Terminal where `python main.py` runs
- **Extension**: Help → Toggle Developer Tools → Console

## Success!

You now have:
✅ Working backend with API
✅ VS Code extension loaded
✅ Symbol search and navigation
✅ Code highlighting
✅ Command interface

Enjoy debugging with your voice! 🎙️
