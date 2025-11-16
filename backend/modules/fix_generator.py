"""
AI-Powered Fix Generation
Uses GPT-4 to generate code fixes
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI

def generate_fix(file_path: str, error: Dict[str, Any], context: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a fix for a code error using GPT-4
    
    Args:
        file_path: Path to file with error
        error: Error dict with line, message, etc.
        context: Optional code context
    
    Returns:
        Dict with diff, rationale, risk_level
    """
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        return {
            "diff": "# OpenAI API key required for fix generation",
            "rationale": "Set OPENAI_API_KEY in .env to enable AI-powered fixes",
            "risk_level": "unknown"
        }
    
    try:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Get context around error
        error_line = error.get('line', 1)
        start = max(0, error_line - 5)
        end = min(len(lines), error_line + 5)
        code_context = ''.join(lines[start:end])
        
        # Build prompt
        prompt = f"""Fix this Python code error:

File: {file_path}
Line {error_line}: {error.get('message', 'Unknown error')}

Code context:
```python
{code_context}
```

Provide:
1. A unified diff showing the fix
2. Brief explanation of what was wrong
3. Risk level (low/medium/high)

Output as JSON:
{{
  "diff": "unified diff format",
  "rationale": "explanation",
  "risk_level": "low|medium|high"
}}
"""
        
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a code fixing assistant. Generate minimal, safe fixes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    
    except Exception as e:
        return {
            "diff": f"# Error generating fix: {str(e)}",
            "rationale": "Fix generation failed",
            "risk_level": "unknown"
        }
