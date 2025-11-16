# EchoDebug VS Code Extension

Voice-controlled AI debugger for Visual Studio Code.

## Features

- 🎙️ Voice command interface (Ctrl+Shift+V)
- 🔍 Find symbols and navigate code
- 🐛 Error detection and explanation
- 🧠 AI-powered code intelligence
- ⚡ Fast symbol indexing
- 💡 Inline code highlighting

## Setup

1. Install dependencies:
```bash
cd vscode-extension
npm install
```

2. Compile TypeScript:
```bash
npm run compile
```

3. Start backend server:
```bash
cd ../backend
python main.py
```

4. Press F5 in VS Code to launch Extension Development Host

## Usage

### Voice Commands (Text Input for now)

Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac) to start a voice command:

- "find all errors in main.py"
- "explain what parse_intent does"
- "where is userData modified"
- "run tests"
- "find symbol handleClick"

### Commands

- `EchoDebug: Start Voice Command` - Start voice input
- `EchoDebug: Explain Selection` - Explain selected code
- `EchoDebug: Find Symbol` - Search for symbol
- `EchoDebug: Build Code Index` - Rebuild symbol index
- `EchoDebug: Show Panel` - Show EchoDebug panel

## Configuration

- `echodebug.backendUrl` - Backend server URL (default: http://localhost:8000)
- `echodebug.highlightColor` - Color for code highlights
- `echodebug.enableVoiceFeedback` - Enable TTS responses

## Development

Watch mode for auto-compilation:
```bash
npm run watch
```

## Note

Voice recording is currently a placeholder. Commands are entered via text input.
Real voice recording will be added in a future update.
