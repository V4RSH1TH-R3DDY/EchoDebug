# Testing the VS Code Extension

## Setup

1. **Start Backend**
```bash
cd backend
python main.py
```

2. **Install Extension Dependencies**
```bash
cd vscode-extension
npm install
npm run compile
```

3. **Launch Extension**
- Open `vscode-extension` folder in VS Code
- Press `F5` to launch Extension Development Host
- A new VS Code window opens with extension loaded

## Test Scenarios

### Test 1: Check Extension Loaded
1. Look for microphone icon in status bar (bottom-right)
2. Should show "🎤 EchoDebug"
3. Tooltip should show connection status

### Test 2: Find Symbol
1. Open any Python file in your project
2. Press `Ctrl+Shift+V` (or click status bar icon)
3. Enter: `find symbol FastAPI`
4. Should show quick pick with results
5. Select one → navigates to location
6. Code should be highlighted in yellow

### Test 3: Explain Selection
1. Select some code in editor
2. Open Command Palette (`Ctrl+Shift+P`)
3. Run: `EchoDebug: Explain Selection`
4. Should show explanation panel

### Test 4: Build Index
1. Command Palette → `EchoDebug: Build Code Index`
2. Should show notification with stats
3. Check backend logs for index building

### Test 5: Show Panel
1. Command Palette → `EchoDebug: Show Panel`
2. Webview panel should open
3. Shows command history

### Test 6: Various Commands

Try these commands via `Ctrl+Shift+V`:

- `find all errors in main.py`
- `explain what parse_intent does`
- `where is userData modified`
- `run tests`
- `find symbol search_code`

## Expected Behavior

### Symbol Search
- Shows quick pick with all matches
- Format: `symbol_name (kind in file:line)`
- Selecting navigates to location
- All occurrences highlighted

### Error Finding
- Shows "Not yet implemented" message
- (Will be enhanced in Phase 5)

### Code Explanation
- Opens webview panel
- Shows explanation text
- (Will use GPT-4 when API key added)

### Test Running
- Opens Output channel
- Shows test results
- Displays exit code

## Troubleshooting

### Extension not appearing
- Check Extensions view (`Ctrl+Shift+X`)
- Should see "EchoDebug [Development]"
- Check Output → Extension Host for errors

### Backend not connecting
- Status bar icon will have red background
- Check backend is running: `curl http://localhost:8000`
- Verify URL in settings: `echodebug.backendUrl`

### Commands not working
- Open Developer Tools: Help → Toggle Developer Tools
- Check Console for errors
- Verify backend logs show requests

### No results found
- Build index first: `EchoDebug: Build Code Index`
- Check backend index stats: `curl http://localhost:8000/index/stats`
- Ensure you're in a Python project

## Demo Flow

**Complete Demo (5 minutes):**

1. **Show Status Bar** (10s)
   - Point out microphone icon
   - Show connection status

2. **Find Symbol** (60s)
   - `Ctrl+Shift+V`
   - "find symbol parse_intent"
   - Show quick pick
   - Navigate to location
   - Show highlighting

3. **Explain Code** (30s)
   - Select a function
   - `EchoDebug: Explain Selection`
   - Show explanation panel

4. **Build Index** (30s)
   - Run build command
   - Show stats notification

5. **Show Panel** (30s)
   - Open EchoDebug panel
   - Show command history

6. **Multiple Commands** (90s)
   - Try 3-4 different commands
   - Show different result types

7. **Settings** (30s)
   - Open settings
   - Show configuration options

## Success Criteria

✅ Extension loads without errors
✅ Status bar icon appears
✅ Backend connection works
✅ Symbol search returns results
✅ Navigation works
✅ Code highlighting works
✅ Commands execute successfully
✅ Panel displays results
✅ Settings are accessible

## Known Limitations

- Voice input is text-based (recording not implemented)
- Some intents show placeholder messages
- TTS not implemented
- Diff view not implemented (Phase 6)

## Next Steps After Testing

If all tests pass:
1. ✅ Phase 4 complete!
2. Ready for Phase 5 (Runtime Debugging)
3. Or enhance with real voice recording
4. Or add GPT-4 integration for better intent parsing
