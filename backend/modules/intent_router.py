"""
Intent Router - Maps intents to handler functions
Provides guardrails for destructive operations
"""

from typing import Dict, Any, Callable, Optional
from .intent_schema import IntentType, Intent
import logging

logger = logging.getLogger(__name__)

class IntentRouter:
    """Routes intents to appropriate handlers with safety checks"""
    
    def __init__(self):
        self.handlers: Dict[IntentType, Callable] = {}
        self.destructive_intents = {
            IntentType.APPLY_FIX,
            IntentType.RENAME_SYMBOL,
            IntentType.FORMAT_FILE
        }
    
    def register_handler(self, intent_type: IntentType, handler: Callable):
        """Register a handler function for an intent"""
        self.handlers[intent_type] = handler
        logger.info(f"Registered handler for {intent_type.value}")
    
    def route(self, intent: Intent, require_confirmation: bool = True) -> Dict[str, Any]:
        """
        Route intent to appropriate handler
        
        Args:
            intent: Parsed intent object
            require_confirmation: Whether to require confirmation for destructive ops
        
        Returns:
            Handler result or confirmation request
        """
        # Check if intent requires confirmation
        if self._is_destructive(intent) and require_confirmation:
            return {
                "status": "confirmation_required",
                "intent": intent.intent,
                "message": f"This action will modify code. Confirm to proceed.",
                "entities": intent.entities.dict()
            }
        
        # Get handler
        handler = self.handlers.get(intent.intent)
        
        if not handler:
            return {
                "status": "error",
                "message": f"No handler registered for intent: {intent.intent}"
            }
        
        # Execute handler
        try:
            logger.info(f"Routing intent: {intent.intent}")
            result = handler(intent.entities)
            return {
                "status": "success",
                "intent": intent.intent,
                "result": result
            }
        except Exception as e:
            logger.error(f"Handler error for {intent.intent}: {str(e)}")
            return {
                "status": "error",
                "intent": intent.intent,
                "message": str(e)
            }
    
    def _is_destructive(self, intent: Intent) -> bool:
        """Check if intent is destructive (modifies code)"""
        return intent.intent in self.destructive_intents
    
    def get_registered_intents(self) -> list:
        """Get list of registered intent types"""
        return list(self.handlers.keys())

# Global router instance
_router = IntentRouter()

def get_router() -> IntentRouter:
    """Get the global intent router"""
    return _router

def register_handlers():
    """Register all default handlers"""
    from .code_parser import search_code, find_symbols
    from .debugger_interface import run_command, explain_trace
    
    router = get_router()
    
    # Register handlers
    router.register_handler(
        IntentType.FIND_SYMBOL,
        lambda entities: find_symbols(entities.symbol or "", entities.language)
    )
    
    router.register_handler(
        IntentType.FIND_ERRORS,
        lambda entities: _find_errors_handler(entities)
    )
    
    router.register_handler(
        IntentType.EXPLAIN_CODE,
        lambda entities: _explain_code_handler(entities)
    )
    
    router.register_handler(
        IntentType.RUN_TESTS,
        lambda entities: _run_tests_handler(entities)
    )
    
    # Add more handlers as needed

def _find_errors_handler(entities) -> Dict[str, Any]:
    """Handler for finding errors"""
    from .linter import find_errors
    
    if entities.file:
        result = find_errors(entities.file, entities.language)
        return result
    
    return {
        "errors": [],
        "warnings": [],
        "message": "Please specify a file to check"
    }

def _explain_code_handler(entities) -> Dict[str, Any]:
    """Handler for explaining code"""
    # TODO: Integrate with LLM for code explanation
    return {
        "message": "Code explanation not yet implemented",
        "target": entities.function or entities.file or "selection"
    }

def _run_tests_handler(entities) -> Dict[str, Any]:
    """Handler for running tests"""
    from .debugger_interface import run_command
    
    # Detect test framework and run
    if entities.language == "python":
        cmd = "pytest -v" if not entities.file else f"pytest {entities.file} -v"
    elif entities.language in ["javascript", "typescript"]:
        cmd = "npm test"
    else:
        return {"message": f"Test running not supported for {entities.language}"}
    
    result = run_command(cmd, timeout=60)
    return result
