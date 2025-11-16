"""
Code Linting and Error Detection
Integrates with pylint, mypy, and other linters
"""

import subprocess
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

def find_errors(file_path: str, language: str = "python") -> Dict[str, Any]:
    """
    Find syntax and semantic errors in a file
    
    Args:
        file_path: Path to file to check
        language: Programming language
    
    Returns:
        Dict with errors, warnings, and suggestions
    """
    if language == "python":
        return _find_python_errors(file_path)
    elif language in ["javascript", "typescript"]:
        return _find_js_errors(file_path)
    else:
        return {
            "errors": [],
            "warnings": [],
            "message": f"Linting not supported for {language}"
        }

def _find_python_errors(file_path: str) -> Dict[str, Any]:
    """Find Python errors using pylint and mypy"""
    errors = []
    warnings = []
    
    # Check if file exists
    if not os.path.exists(file_path):
        return {
            "errors": [{"message": f"File not found: {file_path}", "line": 0}],
            "warnings": [],
            "total_errors": 1,
            "total_warnings": 0
        }
    
    # Run pylint
    try:
        result = subprocess.run(
            ["pylint", file_path, "--output-format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            pylint_results = json.loads(result.stdout)
            
            for issue in pylint_results:
                item = {
                    "line": issue.get("line", 0),
                    "column": issue.get("column", 0),
                    "message": issue.get("message", ""),
                    "type": issue.get("type", ""),
                    "symbol": issue.get("symbol", ""),
                    "source": "pylint"
                }
                
                if issue.get("type") in ["error", "fatal"]:
                    errors.append(item)
                else:
                    warnings.append(item)
    
    except subprocess.TimeoutExpired:
        warnings.append({
            "message": "Pylint timed out",
            "line": 0,
            "source": "pylint"
        })
    except FileNotFoundError:
        warnings.append({
            "message": "Pylint not installed. Install with: pip install pylint",
            "line": 0,
            "source": "system"
        })
    except Exception as e:
        warnings.append({
            "message": f"Pylint error: {str(e)}",
            "line": 0,
            "source": "pylint"
        })
    
    # Run mypy for type checking
    try:
        result = subprocess.run(
            ["mypy", file_path, "--show-column-numbers", "--no-error-summary"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if ':' in line and 'error:' in line:
                    # Parse mypy output: file.py:line:col: error: message
                    parts = line.split(':', 3)
                    if len(parts) >= 4:
                        errors.append({
                            "line": int(parts[1]) if parts[1].isdigit() else 0,
                            "column": int(parts[2]) if parts[2].isdigit() else 0,
                            "message": parts[3].strip(),
                            "type": "type-error",
                            "source": "mypy"
                        })
    
    except subprocess.TimeoutExpired:
        warnings.append({
            "message": "Mypy timed out",
            "line": 0,
            "source": "mypy"
        })
    except FileNotFoundError:
        # Mypy not installed, skip silently
        pass
    except Exception as e:
        warnings.append({
            "message": f"Mypy error: {str(e)}",
            "line": 0,
            "source": "mypy"
        })
    
    # Basic syntax check
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        compile(source, file_path, 'exec')
    except SyntaxError as e:
        errors.append({
            "line": e.lineno or 0,
            "column": e.offset or 0,
            "message": f"Syntax error: {e.msg}",
            "type": "syntax-error",
            "source": "python"
        })
    except Exception as e:
        errors.append({
            "line": 0,
            "column": 0,
            "message": f"Parse error: {str(e)}",
            "type": "parse-error",
            "source": "python"
        })
    
    return {
        "file": file_path,
        "errors": errors,
        "warnings": warnings,
        "total_errors": len(errors),
        "total_warnings": len(warnings)
    }

def _find_js_errors(file_path: str) -> Dict[str, Any]:
    """Find JavaScript/TypeScript errors using eslint"""
    errors = []
    warnings = []
    
    try:
        # Try eslint
        result = subprocess.run(
            ["eslint", file_path, "--format=json"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.stdout:
            eslint_results = json.loads(result.stdout)
            
            for file_result in eslint_results:
                for message in file_result.get("messages", []):
                    item = {
                        "line": message.get("line", 0),
                        "column": message.get("column", 0),
                        "message": message.get("message", ""),
                        "rule": message.get("ruleId", ""),
                        "source": "eslint"
                    }
                    
                    if message.get("severity") == 2:
                        errors.append(item)
                    else:
                        warnings.append(item)
    
    except FileNotFoundError:
        warnings.append({
            "message": "ESLint not installed",
            "line": 0,
            "source": "system"
        })
    except Exception as e:
        warnings.append({
            "message": f"ESLint error: {str(e)}",
            "line": 0,
            "source": "eslint"
        })
    
    return {
        "file": file_path,
        "errors": errors,
        "warnings": warnings,
        "total_errors": len(errors),
        "total_warnings": len(warnings)
    }

def suggest_fix(error: Dict[str, Any], file_path: str) -> Optional[str]:
    """
    Suggest a fix for a specific error
    
    Args:
        error: Error dict with line, message, etc.
        file_path: Path to file
    
    Returns:
        Suggested fix as a string
    """
    # TODO: Use GPT-4 to generate intelligent fixes
    # For now, return basic suggestions
    
    message = error.get("message", "").lower()
    
    if "undefined" in message or "not defined" in message:
        return "Check if the variable is imported or defined before use"
    elif "syntax error" in message:
        return "Check for missing colons, parentheses, or brackets"
    elif "indentation" in message:
        return "Fix indentation to match Python style (4 spaces)"
    elif "type" in message:
        return "Check type annotations and ensure types match"
    
    return None
