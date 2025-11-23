# EchoDebug Web Frontend - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ installed
- EchoDebug backend running on port 8000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Visit **http://localhost:5173**

### Production Build

```bash
npm run build
npm run preview
```

---

## 🎙️ How to Use

1. **Allow Microphone Access** when prompted
2. **Press and Hold** the microphone button (or spacebar)
3. **Speak** your debugging command
4. **Release** to process

### Example Commands
- "Find all errors in main.py"
- "Search for the parse_intent function"
- "Show me where userData is modified"

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/      # UI components
│   ├── services/        # API & audio
│   ├── hooks/           # React hooks
│   ├── types/           # TypeScript types
│   ├── App.tsx          # Main app
│   └── index.css        # Design system
├── .env                 # Config
└── package.json         # Dependencies
```

---

## ✨ Features

- 🎙️ Voice recording with push-to-talk
- 🧠 AI-powered intent parsing
- 🔍 Symbol search and navigation
- 🐛 Error detection and display
- 🔧 AI-generated code fixes
- 📜 Command history with replay
- 🌙 Premium dark theme

---

## 🔧 Configuration

Edit `.env` file:
```bash
VITE_API_URL=http://localhost:8000
```

---

## 🌐 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

Requires microphone permissions.

---

## 📖 Full Documentation

See [README.md](file:///c:/Users/bhava/EchoDebug/frontend/README.md) for complete documentation.
