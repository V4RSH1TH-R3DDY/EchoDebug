# EchoDebug Backend

FastAPI backend for EchoDebug voice-controlled debugger.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

4. Run server:
```bash
python main.py
```

Server runs at http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints

- `POST /stt` - Speech to text conversion
- `POST /intent` - Parse natural language intent
- `POST /search` - Search codebase
- `POST /symbols` - Find symbol definitions
- `POST /run` - Execute commands
- `POST /explain-trace` - Analyze stack traces
- `POST /propose-fix` - Generate code fixes
- `POST /apply-fix` - Apply code modifications

## Development Status

This is Phase 1 scaffold. Core modules are stubs that need implementation:
- `speech_to_text.py` - Add Whisper integration
- `ai_reasoning.py` - Add OpenAI GPT integration
- `code_parser.py` - Enhance AST analysis
- `debugger_interface.py` - Add pdb/debugger hooks
