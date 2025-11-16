import subprocess
import os
from typing import Dict, Any, Optional, List

def run_command(cmd: str, env: Optional[Dict[str, str]] = None, timeout: int = 20) -> Dict[str, Any]:
    """
    Execute shell command and capture output.
    
    Args:
        cmd: Command to execute
        env: Environment variables
        timeout: Timeout in seconds
    
    Returns:
        Dict with exit code, stdout, stderr
    """
    try:
        # Merge environment
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)
        
        # Run command
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=exec_env
        )
        
        return {
            "exit": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    
    except subprocess.TimeoutExpired:
        return {
            "exit": -1,
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds"
        }
    except Exception as e:
        return {
            "exit": -1,
            "stdout": "",
            "stderr": str(e)
        }

def explain_trace(trace: str, snippets: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Analyze stack trace and provide explanation.
    
    Args:
        trace: Stack trace text
        snippets: Optional code snippets for context
    
    Returns:
        Dict with summary and suspect locations
    """
    # TODO: Implement LLM-based trace analysis
    
    # Parse stack trace for file:line references
    suspects = _parse_stack_trace(trace)
    
    return {
        "summary": "Stack trace analysis not yet implemented",
        "suspects": suspects,
        "root_cause": None,
        "suggestions": []
    }

def _parse_stack_trace(trace: str) -> List[Dict[str, Any]]:
    """Extract file and line numbers from stack trace"""
    import re
    
    suspects = []
    
    # Python stack trace pattern: File "path", line X
    python_pattern = r'File "([^"]+)", line (\d+)'
    matches = re.findall(python_pattern, trace)
    
    for file_path, line_num in matches:
        suspects.append({
            "file": file_path,
            "line": int(line_num),
            "language": "python"
        })
    
    # JavaScript stack trace pattern: at ... (path:line:col)
    js_pattern = r'\(([^:]+):(\d+):(\d+)\)'
    js_matches = re.findall(js_pattern, trace)
    
    for file_path, line_num, col_num in js_matches:
        suspects.append({
            "file": file_path,
            "line": int(line_num),
            "column": int(col_num),
            "language": "javascript"
        })
    
    return suspects

def run_python_debugger(script_path: str, breakpoints: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Run Python script with pdb debugger.
    
    Args:
        script_path: Path to Python script
        breakpoints: Optional line numbers for breakpoints
    
    Returns:
        Debugger session info
    """
    # TODO: Implement pdb integration
    return {
        "status": "not_implemented",
        "message": "Python debugger integration pending"
    }
