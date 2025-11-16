"""
Intent Pattern Matching - Robust voice command detection
Handles various phrasings and natural language variations
"""

import re
from typing import Dict, List, Tuple, Optional
from .intent_schema import IntentType, SymbolScope

class IntentPattern:
    """Pattern matcher for intent detection"""
    
    def __init__(self, intent: IntentType, patterns: List[str], priority: int = 1):
        self.intent = intent
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.priority = priority
    
    def match(self, text: str) -> Optional[float]:
        """
        Check if text matches this intent pattern
        Returns confidence score (0.0-1.0) or None
        """
        for pattern in self.patterns:
            if pattern.search(text):
                # Higher priority = higher confidence
                return min(0.95, 0.7 + (self.priority * 0.05))
        return None

# Comprehensive intent patterns
INTENT_PATTERNS = [
    # FIND_ERRORS - High priority
    IntentPattern(IntentType.FIND_ERRORS, [
        r'\b(find|show|check|detect|locate|search)\s+(for\s+)?(all\s+)?(syntax|runtime|logical|type)?\s*(error|bug|issue|problem|mistake)',
        r'\b(what\'?s|whats)\s+(wrong|broken|the\s+error|the\s+issue|the\s+problem)',
        r'\b(check|validate|verify|lint|analyze)\s+(this\s+)?(code|file|script)',
        r'\b(debug|diagnose|troubleshoot)',
        r'\b(any|got|have)\s+(error|bug|issue|problem)',
        r'\b(why\s+is\s+this|why\s+isn\'?t\s+this)\s+(working|running)',
        r'\b(syntax|type|runtime)\s+check',
    ], priority=3),
    
    # FIND_SYMBOL - High priority
    IntentPattern(IntentType.FIND_SYMBOL, [
        r'\b(find|show|locate|search|where)\s+(is|are|the)?\s*\w+\s+(defined|declared|used|called|modified|changed|written|read)',
        r'\b(where|show\s+me)\s+(is|are|does|do)?\s*\w+\s+(get|gets|is)?\s*(defined|declared|used|modified|changed|set|assigned)',
        r'\b(show|find|list)\s+(all\s+)?(uses|usages|references|calls|occurrences)\s+of',
        r'\b(show\s+me\s+all|find\s+all)\s+(uses|references|occurrences)',
        r'\b(go\s+to|jump\s+to|navigate\s+to)\s+(the\s+)?(definition|declaration)\s+of',
        r'\b(what|which)\s+(file|files|line|lines)\s+(use|uses|reference|references|call|calls)',
        r'\b(track|trace|follow)\s+(the\s+)?(symbol|variable|function)',
        r'\b(where|locate)\s+\w+\s+(function|variable|class)',
        r'\b(show\s+references\s+to)',
    ], priority=3),
    
    # EXPLAIN_CODE - Medium-high priority
    IntentPattern(IntentType.EXPLAIN_CODE, [
        r'\b(explain|describe|tell\s+me|what\s+does|what\'?s)\s+(this|the|that)?\s*(code|function|class|method|script|file|line)',
        r'\b(how\s+does|how\s+is)\s+(this|the|that)?\s*(work|working|function|operate)',
        r'\b(what\s+is|what\'?s)\s+(this|the|that)?\s*(doing|for|about)',
        r'\b(help\s+me\s+understand|can\s+you\s+explain|walk\s+me\s+through)',
        r'\b(summarize|summary\s+of)\s+(this|the|that)?\s*(code|function|class)',
        r'\b(break\s+down|break\s+it\s+down)',
    ], priority=2),
    
    # EXPLAIN_TRACE - High priority for errors
    IntentPattern(IntentType.EXPLAIN_TRACE, [
        r'\b(explain|analyze|interpret|decode)\s+(this|the|that)?\s*(error|exception|stack\s+trace|traceback)',
        r'\b(what\s+caused|why\s+did)\s+(this|the|that)?\s*(error|exception|crash|fail)',
        r'\b(why\s+is\s+it|why\s+am\s+i\s+getting)\s+(this|the|that)?\s*(error|exception)',
        r'\b(what\s+does\s+this\s+error\s+mean)',
        r'\b(root\s+cause|what\s+went\s+wrong)',
        r'\b(stack\s+trace|traceback)\s+(analysis|explanation)',
    ], priority=3),
    
    # RUN_TESTS - Medium priority
    IntentPattern(IntentType.RUN_TESTS, [
        r'\b(run|execute|start|perform)\s+(the\s+)?(unit\s+)?(test|tests|testing)',
        r'\b(test\s+this|test\s+the)\s+(code|file|function|class)',
        r'\b(run\s+pytest|run\s+jest|run\s+mocha|run\s+unittest)',
        r'\b(check\s+if\s+tests\s+pass)',
        r'\b(verify\s+with\s+tests)',
    ], priority=2),
    
    # PROPOSE_FIX - High priority (but lower than FORMAT for "fix formatting")
    IntentPattern(IntentType.PROPOSE_FIX, [
        r'\b(fix|correct|repair|resolve|solve)\s+(this|the|that)?\s*(error|bug|issue|problem|code)',
        r'\b(how\s+do\s+i\s+fix|how\s+to\s+fix|how\s+can\s+i\s+fix)',
        r'\b(suggest|propose|recommend)\s+(a\s+)?(fix|solution|correction)',
        r'\b(make\s+it\s+work|get\s+it\s+working)',
        r'\b(auto\s+fix|quick\s+fix)',
        r'\brepair\s+(this|the)',
    ], priority=2),
    
    # FORMAT_FILE - Medium priority
    IntentPattern(IntentType.FORMAT_FILE, [
        r'\b(format|prettify|beautify|clean\s+up)\s+(this|the|that|my)?\s*(code|file)',
        r'\b(make\s+it\s+)?(prettier|cleaner|readable)',
        r'\b(auto\s+format|reformat)',
        r'\b(apply\s+)?(code\s+style|style\s+guide)',
        r'\bprettify\b',
        r'\bbeautify\b',
    ], priority=2),
    
    # RENAME_SYMBOL - Medium priority
    IntentPattern(IntentType.RENAME_SYMBOL, [
        r'\b(rename|change)\s+\w+\s+(to|into)\s+\w+',
        r'\b(refactor|update)\s+\w+\s+(to|into|name)',
        r'\b(call\s+it|name\s+it)\s+\w+\s+instead',
        r'\bchange\s+\w+\s+to\s+\w+',
    ], priority=2),
    
    # NAVIGATE_TO - Medium priority
    IntentPattern(IntentType.NAVIGATE_TO, [
        r'\b(go\s+to|jump\s+to|navigate\s+to|open|show\s+me)\s+(line|file|function|class)',
        r'\b(take\s+me\s+to|bring\s+me\s+to)',
        r'\b(open\s+the\s+file)\s+\w+',
    ], priority=2),
    
    # APPLY_FIX - Lower priority (should be explicit)
    IntentPattern(IntentType.APPLY_FIX, [
        r'\b(apply|implement|use|accept)\s+(the|this|that)?\s*(fix|patch|change|solution)',
        r'\b(yes,?\s+fix\s+it|go\s+ahead|do\s+it|make\s+the\s+change)',
    ], priority=1),
]

def detect_intent_from_patterns(text: str) -> Tuple[IntentType, float]:
    """
    Detect intent using pattern matching
    
    Returns:
        (intent_type, confidence_score)
    """
    best_match = None
    best_confidence = 0.0
    
    for pattern in INTENT_PATTERNS:
        confidence = pattern.match(text)
        if confidence and confidence > best_confidence:
            best_match = pattern.intent
            best_confidence = confidence
    
    # Default to EXPLAIN_CODE if no match
    if not best_match:
        return IntentType.EXPLAIN_CODE, 0.5
    
    return best_match, best_confidence

def extract_symbol_from_text(text: str) -> Optional[str]:
    """Extract symbol name from text using various patterns"""
    
    # Pattern: "find where X is/are/gets defined/used/modified"
    patterns = [
        r'\b(?:find|show|where|locate)\s+(?:is|are|the)?\s*(\w+)\s+(?:defined|declared|used|modified|changed)',
        r'\b(?:where|show)\s+(?:is|are|does)?\s*(\w+)\s+(?:get|gets|is)?\s*(?:defined|used|modified|set)',
        r'\b(?:references|uses|calls|occurrences)\s+(?:of|to)\s+(\w+)',
        r'\b(?:symbol|variable|function|class)\s+(?:named|called)?\s*(\w+)',
        r'\b(?:track|trace|follow)\s+(?:the\s+)?(?:symbol\s+)?(\w+)',
        r'\b(?:all\s+uses\s+of|all\s+references\s+to)\s+(\w+)',
        r'\b(?:definition\s+of)\s+(\w+)',
        # Generic: quoted or camelCase/snake_case words (lower priority)
        r'["\'](\w+)["\']',
        r'\b([a-z]+[A-Z]\w+)\b',  # camelCase
        r'\b([a-z]+_[a-z_]+)\b',  # snake_case
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            symbol = match.group(1)
            # Filter out common words
            if symbol.lower() not in ['this', 'that', 'the', 'is', 'are', 'get', 'gets', 'file', 'code', 'where', 'show', 'find', 'all']:
                return symbol
    
    return None

def extract_file_from_text(text: str) -> Optional[str]:
    """Extract filename from text"""
    
    # Pattern: filename with extension
    patterns = [
        r'\b(\w+\.(?:py|js|ts|java|cpp|c|h|jsx|tsx|json|yaml|yml|md))\b',
        r'(?:file|script)\s+(?:named|called)?\s*["\']?(\w+)["\']?',
        r'(?:in|from)\s+["\']?(\w+\.(?:py|js|ts|java))["\']?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def extract_scope_from_text(text: str) -> SymbolScope:
    """Determine if looking for reads, writes, or all references"""
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['modified', 'changed', 'written', 'set', 'assigned', 'updated']):
        return SymbolScope.WRITES
    elif any(word in text_lower for word in ['read', 'accessed', 'used', 'referenced']):
        return SymbolScope.READS
    elif any(word in text_lower for word in ['defined', 'declared', 'created']):
        return SymbolScope.DECLARATIONS
    
    return SymbolScope.ALL

def extract_line_number(text: str) -> Optional[int]:
    """Extract line number from text"""
    
    patterns = [
        r'\bline\s+(\d+)\b',
        r'\bat\s+line\s+(\d+)\b',
        r'\bon\s+line\s+(\d+)\b',
        r'\b:(\d+)\b',  # file.py:42
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return int(match.group(1))
    
    return None

def extract_function_name(text: str) -> Optional[str]:
    """Extract function name from text"""
    
    patterns = [
        r'\bfunction\s+(?:named|called)?\s*(\w+)',
        r'\bmethod\s+(?:named|called)?\s*(\w+)',
        r'\bdef\s+(\w+)',
        r'\b(\w+)\s+function',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def detect_language_from_text(text: str) -> str:
    """Detect programming language from text"""
    
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['python', '.py', 'pytest', 'django', 'flask']):
        return "python"
    elif any(word in text_lower for word in ['javascript', 'js', '.js', 'node', 'npm', 'react']):
        return "javascript"
    elif any(word in text_lower for word in ['typescript', 'ts', '.ts', 'tsx']):
        return "typescript"
    elif any(word in text_lower for word in ['java', '.java', 'spring', 'maven']):
        return "java"
    
    # Default to python
    return "python"
