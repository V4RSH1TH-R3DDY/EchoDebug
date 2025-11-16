import os
import ast
import re
from typing import List, Dict, Any
from pathlib import Path

def search_code(query: str, lang: str = "python", scope: str = "all") -> List[Dict[str, Any]]:
    """
    Search codebase for query string.
    
    Args:
        query: Search query
        lang: Programming language
        scope: Search scope (all, functions, classes, etc.)
    
    Returns:
        List of search results with file, line, preview
    """
    results = []
    
    # Get workspace root (for now, use current directory)
    workspace = Path.cwd()
    
    # File patterns by language
    patterns = {
        "python": "**/*.py",
        "javascript": "**/*.js",
        "typescript": "**/*.ts",
        "java": "**/*.java"
    }
    
    pattern = patterns.get(lang, "**/*.*")
    
    try:
        for file_path in workspace.glob(pattern):
            if _should_ignore(file_path):
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    if query.lower() in line.lower():
                        results.append({
                            "file": str(file_path.relative_to(workspace)),
                            "line": line_num,
                            "preview": line.strip(),
                            "context": _get_context(lines, line_num)
                        })
            except Exception:
                continue
    
    except Exception as e:
        raise Exception(f"Search error: {str(e)}")
    
    return results[:50]  # Limit results

def find_symbols(name: str, lang: str = "python", use_index: bool = True) -> List[Dict[str, Any]]:
    """
    Find symbol definitions and references.
    
    Args:
        name: Symbol name to find
        lang: Programming language
        use_index: Use code index for faster search
    
    Returns:
        List of symbol locations
    """
    if use_index and lang == "python":
        # Try using index first
        try:
            from .code_index import get_index
            index = get_index()
            results = index.search_symbols(name)
            if results:
                return results
        except Exception as e:
            # Fall back to AST search
            pass
    
    if lang == "python":
        return _find_python_symbols(name)
    else:
        # Fallback to regex search
        return search_code(name, lang)

def _find_python_symbols(name: str) -> List[Dict[str, Any]]:
    """Find Python symbols using AST"""
    results = []
    workspace = Path.cwd()
    
    for file_path in workspace.glob("**/*.py"):
        if _should_ignore(file_path):
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
                tree = ast.parse(source)
            
            for node in ast.walk(tree):
                # Function definitions
                if isinstance(node, ast.FunctionDef) and node.name == name:
                    results.append({
                        "file": str(file_path.relative_to(workspace)),
                        "line": node.lineno,
                        "kind": "function",
                        "preview": f"def {node.name}(...)"
                    })
                
                # Class definitions
                elif isinstance(node, ast.ClassDef) and node.name == name:
                    results.append({
                        "file": str(file_path.relative_to(workspace)),
                        "line": node.lineno,
                        "kind": "class",
                        "preview": f"class {node.name}"
                    })
                
                # Variable assignments
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == name:
                            results.append({
                                "file": str(file_path.relative_to(workspace)),
                                "line": node.lineno,
                                "kind": "assignment",
                                "preview": f"{name} = ..."
                            })
        
        except Exception:
            continue
    
    return results

def _should_ignore(path: Path) -> bool:
    """Check if path should be ignored"""
    ignore_patterns = [
        ".git", "__pycache__", "node_modules", ".venv", "venv",
        "dist", "build", ".pytest_cache", ".mypy_cache"
    ]
    
    return any(pattern in str(path) for pattern in ignore_patterns)

def _get_context(lines: List[str], line_num: int, context_size: int = 2) -> List[str]:
    """Get surrounding lines for context"""
    start = max(0, line_num - context_size - 1)
    end = min(len(lines), line_num + context_size)
    return [line.strip() for line in lines[start:end]]
