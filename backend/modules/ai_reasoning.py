import os
from typing import Dict, Any, Optional
import json
from .intent_schema import Intent, IntentType, IntentEntities, get_intent_prompt, validate_intent
from .intent_patterns import (
    detect_intent_from_patterns,
    extract_symbol_from_text,
    extract_file_from_text,
    extract_scope_from_text,
    extract_line_number,
    extract_function_name,
    detect_language_from_text
)

# OpenAI client
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

def parse_intent(text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Parse natural language into structured intent using LLM.
    
    Args:
        text: User's natural language command
        context: Optional context (file list, recent actions, etc.)
    
    Returns:
        Intent JSON with intent, confidence, entities
    """
    # Check if OpenAI API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key and api_key != "your_api_key_here":
        # Use OpenAI GPT for intent parsing
        try:
            return _parse_intent_with_llm(text, context)
        except Exception as e:
            print(f"LLM parsing failed, falling back to keyword matching: {e}")
            return _parse_intent_fallback(text)
    else:
        # Fallback to keyword matching
        return _parse_intent_fallback(text)

def _parse_intent_with_llm(text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Parse intent using OpenAI GPT"""
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Build context string
    context_str = ""
    if context:
        if "files" in context:
            context_str += f"\nAvailable files: {', '.join(context['files'][:10])}"
        if "current_file" in context:
            context_str += f"\nCurrent file: {context['current_file']}"
    
    system_prompt = get_intent_prompt()
    user_prompt = f"User command: {text}{context_str}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using mini for speed and cost
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        intent_data = json.loads(response.choices[0].message.content)
        
        # Validate and return
        validated = validate_intent(intent_data)
        return validated.dict()
    
    except Exception as e:
        print(f"LLM parsing error: {e}")
        # Fall back to keyword matching
        return _parse_intent_fallback(text)

def _parse_intent_fallback(text: str) -> Dict[str, Any]:
    """Enhanced pattern-based intent parsing"""
    
    # Use pattern matching for intent detection
    intent, confidence = detect_intent_from_patterns(text)
    
    # Extract entities using specialized extractors
    entities = IntentEntities(
        file=extract_file_from_text(text),
        symbol=extract_symbol_from_text(text),
        language=detect_language_from_text(text),
        scope=extract_scope_from_text(text),
        line=extract_line_number(text),
        function=extract_function_name(text)
    )
    
    # Create validated intent
    intent_obj = Intent(
        intent=intent,
        confidence=confidence,
        entities=entities,
        follow_up_allowed=True,
        raw_text=text
    )
    
    return intent_obj.dict()

def _extract_file_entity(text: str) -> Dict[str, Any]:
    """Extract file name from text"""
    # Simple extraction - improve with NER
    words = text.split()
    for word in words:
        if ".py" in word or ".js" in word or ".java" in word:
            return {"file": word.strip("\"'"), "language": _detect_language(word)}
    return {"file": None, "language": "python"}

def _extract_symbol_entity(text: str) -> Dict[str, Any]:
    """Extract symbol name from text"""
    # Look for quoted strings or camelCase/snake_case identifiers
    words = text.split()
    for i, word in enumerate(words):
        if word in ["where", "find", "symbol"]:
            if i + 1 < len(words):
                symbol = words[i + 1].strip("\"'")
                return {
                    "symbol": symbol,
                    "scope": "all",
                    "language": "python"
                }
    return {"symbol": None, "scope": "all", "language": "python"}

def _extract_code_entity(text: str) -> Dict[str, Any]:
    """Extract code reference from text"""
    return {"target": "selection", "language": "python"}

def _detect_language(filename: str) -> str:
    """Detect programming language from filename"""
    if filename.endswith(".py"):
        return "python"
    elif filename.endswith((".js", ".ts")):
        return "javascript"
    elif filename.endswith(".java"):
        return "java"
    return "unknown"

def generate_llm_response(prompt: str, system_prompt: Optional[str] = None) -> str:
    """
    Generate response using LLM.
    
    Args:
        prompt: User prompt
        system_prompt: Optional system instructions
    
    Returns:
        LLM response text
    """
    # TODO: Implement OpenAI API call
    # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # response = client.chat.completions.create(...)
    
    return "LLM response placeholder"
