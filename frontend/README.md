# EchoDebug Web Frontend

Modern, voice-controlled debugging interface for EchoDebug.

## Features

- 🎙️ **Voice Recording** - Push-to-talk interface with visual feedback
- 🧠 **Intent Parsing** - AI-powered command understanding
- 🔍 **Symbol Search** - Find functions, classes, and variables
- 🐛 **Error Detection** - Real-time linting and error display
- 🔧 **AI Fixes** - Intelligent code repair suggestions
- 📜 **Command History** - Track and replay previous commands
- 🌙 **Dark Mode** - Premium glassmorphism design

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Backend URL
Create a `.env` file:
```bash
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server
```bash
npm run dev
```

Visit `http://localhost:5173`

## Usage

1. **Start Backend**: Make sure the EchoDebug backend is running on port 8000
2. **Allow Microphone**: Grant microphone permissions when prompted
3. **Press and Hold**: Click or press spacebar to record
4. **Speak Command**: Say your debugging command
5. **Release**: Stop recording to process

### Example Commands

- "Find all errors in main.py"
- "Search for the parse_intent function"
- "Show me where userData is modified"
- "Fix the syntax errors in app.py"

## Build for Production

```bash
npm run build
npm run preview
```

## Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Axios** - HTTP client
- **Web Audio API** - Voice recording

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

Requires microphone access for voice features.

## Project Structure

```
src/
├── components/       # React components
│   ├── VoiceRecorder.tsx
│   ├── ResultsPanel.tsx
│   └── CommandHistory.tsx
├── services/         # API and audio services
│   ├── apiClient.ts
│   └── audioRecorder.ts
├── hooks/            # Custom React hooks
│   ├── useVoiceRecording.ts
│   └── useBackendStatus.ts
├── types/            # TypeScript definitions
│   └── types.ts
├── App.tsx           # Main application
└── index.css         # Design system
```

## License

MIT
