"""
Intent Schema and Validation for EchoDebug
Defines all valid intents and their entity structures
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

class IntentType(str, Enum):
    """Valid intent types"""
    FIND_ERRORS = "find_errors"
    EXPLAIN_CODE = "explain_code"
    FIND_SYMBOL = "find_symbol"
    NAVIGATE_TO = "navigate_to"
    RUN_TESTS = "run_tests"
    EXPLAIN_TRACE = "explain_trace"
    PROPOSE_FIX = "propose_fix"
    APPLY_FIX = "apply_fix"
    FORMAT_FILE = "format_file"
    RENAME_SYMBOL = "rename_symbol"

class SymbolScope(str, Enum):
    """Scope for symbol searches"""
    ALL = "all"
    READS = "reads"
    WRITES = "writes"
    DECLARATIONS = "declarations"

class Language(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    UNKNOWN = "unknown"

class IntentEntities(BaseModel):
    """Entities extracted from user command"""
    file: Optional[str] = None
    symbol: Optional[str] = None
    language: Optional[Language] = Language.PYTHON
    scope: Optional[SymbolScope] = SymbolScope.ALL
    line: Optional[int] = None
    function: Optional[str] = None
    error_type: Optional[str] = None
    
    class Config:
        use_enum_values = True
        # Allow None values for enums
        validate_default = True

class Intent(BaseModel):
    """Structured intent representation"""
    intent: IntentType
    confidence: float = Field(ge=0.0, le=1.0)
    entities: IntentEntities
    follow_up_allowed: bool = True
    raw_text: Optional[str] = None
    
    class Config:
        use_enum_values = True
    
    @validator('confidence')
    def validate_confidence(cls, v):
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0 and 1')
        return v

# Intent descriptions for LLM prompt
INTENT_DESCRIPTIONS = {
    IntentType.FIND_ERRORS: "Find syntax, runtime, or logical errors in code",
    IntentType.EXPLAIN_CODE: "Explain what a piece of code does in natural language",
    IntentType.FIND_SYMBOL: "Find where a symbol (variable, function, class) is defined or used",
    IntentType.NAVIGATE_TO: "Navigate to a specific location in code",
    IntentType.RUN_TESTS: "Execute unit tests or test suites",
    IntentType.EXPLAIN_TRACE: "Explain a stack trace and identify root cause",
    IntentType.PROPOSE_FIX: "Suggest a fix for a code issue",
    IntentType.APPLY_FIX: "Apply a proposed code modification",
    IntentType.FORMAT_FILE: "Format/prettify code according to style guidelines",
    IntentType.RENAME_SYMBOL: "Rename a symbol across the entire codebase"
}

# Example utterances for each intent (for training/testing)
INTENT_EXAMPLES = {
    IntentType.FIND_ERRORS: [
        "find all syntax errors in main.py",
        "check for bugs in this file",
        "what's wrong with my code",
        "show me errors"
    ],
    IntentType.EXPLAIN_CODE: [
        "explain what this function does",
        "what does this code do",
        "describe this class",
        "help me understand this"
    ],
    IntentType.FIND_SYMBOL: [
        "find where userData is defined",
        "show me all uses of counter",
        "where is this variable modified",
        "find references to handleClick"
    ],
    IntentType.RUN_TESTS: [
        "run tests",
        "execute unit tests",
        "test this file",
        "run pytest"
    ],
    IntentType.EXPLAIN_TRACE: [
        "explain this error",
        "what caused this exception",
        "analyze this stack trace",
        "why did this fail"
    ],
    IntentType.PROPOSE_FIX: [
        "fix this error",
        "suggest a solution",
        "how do I fix this",
        "propose a fix for indentation"
    ]
}

def get_intent_prompt() -> str:
    """Generate system prompt for LLM intent classification"""
    intents_list = "\n".join([
        f"- {intent.value}: {desc}"
        for intent, desc in INTENT_DESCRIPTIONS.items()
    ])
    
    return f"""You are an NLU router for EchoDebug, a voice-controlled debugger.
Your job is to classify user commands into structured intents.

Valid intents:
{intents_list}

Output ONLY valid JSON matching this schema:
{{
  "intent": "<intent_type>",
  "confidence": <0.0-1.0>,
  "entities": {{
    "file": "<filename or null>",
    "symbol": "<symbol_name or null>",
    "language": "<python|javascript|typescript|java>",
    "scope": "<all|reads|writes|declarations>",
    "line": <line_number or null>,
    "function": "<function_name or null>",
    "error_type": "<error_type or null>"
  }},
  "follow_up_allowed": <true|false>
}}

Rules:
1. Always output valid JSON
2. Use only the intents listed above
3. Extract all relevant entities from the user's command
4. Set confidence based on clarity of the command
5. If the command is ambiguous, choose the most likely intent
6. Refuse commands outside the scope of debugging/code analysis
"""

def validate_intent(intent_data: Dict[str, Any]) -> Intent:
    """Validate and parse intent data"""
    return Intent(**intent_data)
