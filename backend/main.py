from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from modules.speech_to_text import transcribe_audio, transcribe_audio_file
from modules.ai_reasoning import parse_intent
from modules.code_parser import search_code, find_symbols
from modules.debugger_interface import run_command, explain_trace
from modules.code_index import get_index, rebuild_index
from modules.intent_router import get_router, register_handlers
from modules.intent_schema import Intent, validate_intent
from modules.linter import find_errors
from modules.fix_generator import generate_fix

app = FastAPI(title="EchoDebug API", version="0.1.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize intent router on startup
@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    register_handlers()
    # Try to load existing index
    index = get_index()
    if not index.last_indexed:
        # Build index in background if it doesn't exist
        import threading
        threading.Thread(target=lambda: index.build_index()).start()

# Request/Response Models
class STTRequest(BaseModel):
    audio_data: str  # base64 encoded audio
    format: str = "wav"

class IntentRequest(BaseModel):
    text: str
    context: Optional[Dict[str, Any]] = None

class SearchRequest(BaseModel):
    query: str
    lang: str = "python"
    scope: str = "all"

class SymbolRequest(BaseModel):
    name: str
    lang: str = "python"

class RunRequest(BaseModel):
    cmd: str
    env: Optional[Dict[str, str]] = None
    timeout: int = 20

class ExplainTraceRequest(BaseModel):
    trace: str
    snippets: Optional[List[str]] = None

class ProposeFixRequest(BaseModel):
    file: str
    span: Optional[Dict[str, int]] = None
    goal: str

class ApplyFixRequest(BaseModel):
    diff: str

# Endpoints
@app.get("/")
async def root():
    return {"message": "EchoDebug API", "status": "running"}

@app.post("/stt")
async def speech_to_text(request: STTRequest):
    """Convert speech audio to text"""
    try:
        text = transcribe_audio(request.audio_data, request.format)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/intent")
async def classify_intent(request: IntentRequest):
    """Parse natural language into structured intent"""
    try:
        intent_data = parse_intent(request.text, request.context)
        return intent_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search")
async def search_codebase(request: SearchRequest):
    """Search code based on query"""
    try:
        results = search_code(request.query, request.lang, request.scope)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/symbols")
async def find_symbol(request: SymbolRequest):
    """Find symbol definitions and references"""
    try:
        symbols = find_symbols(request.name, request.lang)
        return {"symbols": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/run")
async def run_code(request: RunRequest):
    """Execute command and capture output"""
    try:
        result = run_command(request.cmd, request.env, request.timeout)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/explain-trace")
async def explain_stack_trace(request: ExplainTraceRequest):
    """Explain stack trace and identify root cause"""
    try:
        explanation = explain_trace(request.trace, request.snippets)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/propose-fix")
async def propose_code_fix(request: ProposeFixRequest):
    """Generate a proposed fix for code issue"""
    try:
        # First, find errors in the file
        errors_result = find_errors(request.file)
        
        if not errors_result.get('errors'):
            return {
                "diff": "# No errors found",
                "rationale": "File has no detected errors",
                "risk_level": "low"
            }
        
        # Generate fix for first error
        first_error = errors_result['errors'][0]
        fix = generate_fix(request.file, first_error)
        
        return fix
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/apply-fix")
async def apply_code_fix(request: ApplyFixRequest):
    """Apply a code fix diff"""
    try:
        # Placeholder - implement in Phase 6
        return {
            "ok": False,
            "files_changed": [],
            "message": "Apply fix not yet implemented"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Phase 2 & 3 endpoints

@app.post("/intent/route")
async def route_intent(request: IntentRequest):
    """Parse intent and route to appropriate handler"""
    try:
        # Parse intent
        intent_data = parse_intent(request.text, request.context)
        intent = validate_intent(intent_data)
        
        # Route to handler
        router = get_router()
        result = router.route(intent)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/index/build")
async def build_index(force: bool = False):
    """Build or rebuild the code index"""
    try:
        stats = rebuild_index(force=force)
        return {"status": "success", "stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/index/stats")
async def get_index_stats():
    """Get code index statistics"""
    try:
        index = get_index()
        return {
            "last_indexed": index.last_indexed.isoformat() if index.last_indexed else None,
            "total_symbols": sum(len(symbols) for symbols in index.symbols.values()),
            "unique_symbols": len(index.symbols),
            "files_indexed": len(index.files)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/symbols/file/{file_path:path}")
async def get_file_symbols(file_path: str):
    """Get all symbols in a specific file"""
    try:
        index = get_index()
        symbols = index.get_file_symbols(file_path)
        return {"file": file_path, "symbols": symbols}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/symbols/{symbol_name}/references")
async def get_symbol_references(symbol_name: str):
    """Get all references to a symbol"""
    try:
        index = get_index()
        references = index.get_symbol_references(symbol_name)
        return {"symbol": symbol_name, "references": references}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lint")
async def lint_file(file: str, lang: str = "python"):
    """Find errors and warnings in a file"""
    try:
        result = find_errors(file, lang)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class STTFileRequest(BaseModel):
    file_path: str

@app.post("/stt/file")
async def speech_to_text_file(request: STTFileRequest):
    """Transcribe audio file to text"""
    try:
        text = transcribe_audio_file(request.file_path)
        return {"text": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
