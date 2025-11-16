# VS Code Extension Setup Guide

## Prerequisites

- Node.js 18+ installed
- VS Code installed
- EchoDebug backend running

## Installation Steps

### 1. Install Dependencies

```bash
cd vscode-extension
npm install
```

### 2. Compile TypeScript

```bash
npm run compile
```

Or watch mode for development:
```bash
npm run watch
```

### 3. Start Backend Server

In a separate terminal:
```bash
cd backend
python main.py
```

### 4. Launch Extension

**Option A: Development Mode (F5)**
1. Open `vscode-extension` folder in VS Code
2. Press `F5` to launch Extension Development Host
3. A new VS Code window will open with the extension loaded

**Option B: Install Locally**
1. Package the extension:
```bash
npm install -g @vscode/vsce
vsce package
```

2. Install the `.vsix` file:
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Click "..." menu → "Install from VSIX"
   - Select the generated `.vsix` file

## Usage

### Quick Start

1. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)
2. Enter a command like "find symbol parse_intent"
3. View results and navigate to code

### Available Commands

Open Command Palette (`Ctrl+Shift+P`) and search for:

- `EchoDebug: Start Voice Command`
- `EchoDebug: Explain Selection`
- `EchoDebug: Find Symbol`
- `EchoDebug: Build Code Index`
- `EchoDebug: Show Panel`
- `EchoDebug: Open Settings`

### Status Bar

Look for the microphone icon in the bottom-right status bar:
- 🎤 EchoDebug - Ready
- 🎤 Listening... - Recording (when implemented)
- Red background - Backend not connected

## Configuration

Open Settings (`Ctrl+,`) and search for "echodebug":

- **Backend URL**: Default `http://localhost:8000`
- **Highlight Color**: Color for code highlights
- **Voice Feedback**: Enable TTS (future feature)

## Troubleshooting

### Extension not loading
- Check VS Code version (requires 1.80+)
- Run `npm run compile` to rebuild
- Check Output panel for errors

### Backend not connecting
- Ensure backend is running on port 8000
- Check `echodebug.backendUrl` setting
- Test backend: `curl http://localhost:8000`

### Commands not working
- Check backend logs for errors
- Verify code index is built
- Try rebuilding index: `EchoDebug: Build Code Index`

## Development

### File Structure

```
vscode-extension/
├── src/
│   ├── extension.ts       # Main extension entry
│   ├── backendClient.ts   # API client
│   ├── codeHighlighter.ts # Code highlighting
│   ├── panel.ts           # Webview panel
│   └── voiceRecorder.ts   # Voice recording (placeholder)
├── package.json           # Extension manifest
├── tsconfig.json          # TypeScript config
└── README.md
```

### Adding New Commands

1. Add command to `package.json` → `contributes.commands`
2. Register handler in `extension.ts` → `activate()`
3. Implement handler function
4. Recompile and reload

### Debugging

1. Set breakpoints in TypeScript files
2. Press F5 to launch debugger
3. Use Debug Console to inspect variables
4. Check Extension Host logs in Output panel

## Next Steps

- [ ] Implement real voice recording
- [ ] Add diff view for code fixes
- [ ] Enhance webview panel UI
- [ ] Add inline diagnostics
- [ ] Implement TTS feedback
