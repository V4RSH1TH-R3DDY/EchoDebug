"""
Code Indexing System - Fast symbol lookup and code intelligence
Builds and maintains an index of code symbols for quick searches
"""

import os
import ast
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class Symbol:
    """Represents a code symbol"""
    name: str
    kind: str  # function, class, variable, import, method
    file: str
    line: int
    column: int = 0
    end_line: Optional[int] = None
    scope: Optional[str] = None  # module, class, function
    language: str = "python"
    signature: Optional[str] = None
    docstring: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class Reference:
    """Represents a symbol reference (read/write)"""
    symbol: str
    file: str
    line: int
    column: int
    ref_type: str  # read, write, call
    context: Optional[str] = None

class CodeIndex:
    """Maintains an index of code symbols for fast lookup"""
    
    def __init__(self, workspace_path: str = "."):
        self.workspace = Path(workspace_path)
        self.symbols: Dict[str, List[Symbol]] = {}  # symbol_name -> [Symbol]
        self.files: Dict[str, str] = {}  # file_path -> file_hash
        self.references: Dict[str, List[Reference]] = {}  # symbol_name -> [Reference]
        self.last_indexed = None
        self.index_file = self.workspace / ".echodebug_index.json"
    
    def build_index(self, force: bool = False) -> Dict[str, Any]:
        """
        Build or update the code index
        
        Args:
            force: Force rebuild even if files haven't changed
        
        Returns:
            Index statistics
        """
        logger.info("Building code index...")
        start_time = datetime.now()
        
        stats = {
            "files_indexed": 0,
            "symbols_found": 0,
            "files_skipped": 0,
            "errors": 0
        }
        
        # Find all code files
        python_files = list(self.workspace.glob("**/*.py"))
        
        for file_path in python_files:
            if self._should_ignore(file_path):
                stats["files_skipped"] += 1
                continue
            
            try:
                # Check if file changed
                file_hash = self._hash_file(file_path)
                rel_path = str(file_path.relative_to(self.workspace))
                
                if not force and rel_path in self.files and self.files[rel_path] == file_hash:
                    stats["files_skipped"] += 1
                    continue
                
                # Index the file
                symbols = self._index_python_file(file_path)
                
                # Store symbols
                for symbol in symbols:
                    if symbol.name not in self.symbols:
                        self.symbols[symbol.name] = []
                    self.symbols[symbol.name].append(symbol)
                    stats["symbols_found"] += 1
                
                self.files[rel_path] = file_hash
                stats["files_indexed"] += 1
                
            except Exception as e:
                logger.error(f"Error indexing {file_path}: {e}")
                stats["errors"] += 1
        
        self.last_indexed = datetime.now()
        duration = (self.last_indexed - start_time).total_seconds()
        
        stats["duration_seconds"] = duration
        logger.info(f"Index built: {stats}")
        
        # Save index to disk
        self._save_index()
        
        return stats
    
    def _index_python_file(self, file_path: Path) -> List[Symbol]:
        """Index a Python file using AST"""
        symbols = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source)
            rel_path = str(file_path.relative_to(self.workspace))
            
            # Walk AST and extract symbols
            for node in ast.walk(tree):
                symbol = None
                
                # Function definitions
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    signature = f"def {node.name}({', '.join(args)})"
                    docstring = ast.get_docstring(node)
                    
                    symbol = Symbol(
                        name=node.name,
                        kind="function",
                        file=rel_path,
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        signature=signature,
                        docstring=docstring,
                        language="python"
                    )
                
                # Class definitions
                elif isinstance(node, ast.ClassDef):
                    bases = [self._get_name(base) for base in node.bases]
                    signature = f"class {node.name}({', '.join(bases)})" if bases else f"class {node.name}"
                    docstring = ast.get_docstring(node)
                    
                    symbol = Symbol(
                        name=node.name,
                        kind="class",
                        file=rel_path,
                        line=node.lineno,
                        column=node.col_offset,
                        end_line=node.end_lineno,
                        signature=signature,
                        docstring=docstring,
                        language="python"
                    )
                
                # Variable assignments (module level)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            symbol = Symbol(
                                name=target.id,
                                kind="variable",
                                file=rel_path,
                                line=node.lineno,
                                column=node.col_offset,
                                language="python"
                            )
                            symbols.append(symbol)
                
                # Imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        symbol = Symbol(
                            name=alias.asname or alias.name,
                            kind="import",
                            file=rel_path,
                            line=node.lineno,
                            column=node.col_offset,
                            signature=f"import {alias.name}",
                            language="python"
                        )
                        symbols.append(symbol)
                
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        symbol = Symbol(
                            name=alias.asname or alias.name,
                            kind="import",
                            file=rel_path,
                            line=node.lineno,
                            column=node.col_offset,
                            signature=f"from {node.module} import {alias.name}",
                            language="python"
                        )
                        symbols.append(symbol)
                
                if symbol and symbol not in symbols:
                    symbols.append(symbol)
        
        except Exception as e:
            logger.error(f"Error parsing {file_path}: {e}")
        
        return symbols
    
    def search_symbols(self, query: str, kind: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search for symbols by name
        
        Args:
            query: Symbol name or pattern
            kind: Filter by symbol kind (function, class, etc.)
            limit: Maximum results
        
        Returns:
            List of matching symbols
        """
        results = []
        query_lower = query.lower()
        
        for name, symbol_list in self.symbols.items():
            if query_lower in name.lower():
                for symbol in symbol_list:
                    if kind and symbol.kind != kind:
                        continue
                    results.append(symbol.to_dict())
                    if len(results) >= limit:
                        return results
        
        return results
    
    def get_symbol_references(self, symbol_name: str) -> List[Dict[str, Any]]:
        """Get all references to a symbol"""
        refs = self.references.get(symbol_name, [])
        return [asdict(ref) for ref in refs]
    
    def get_file_symbols(self, file_path: str) -> List[Dict[str, Any]]:
        """Get all symbols defined in a file"""
        results = []
        for symbol_list in self.symbols.values():
            for symbol in symbol_list:
                if symbol.file == file_path:
                    results.append(symbol.to_dict())
        return results
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored"""
        ignore_patterns = [
            ".git", "__pycache__", "node_modules", ".venv", "venv",
            "dist", "build", ".pytest_cache", ".mypy_cache", ".echodebug_index.json"
        ]
        return any(pattern in str(path) for pattern in ignore_patterns)
    
    def _hash_file(self, file_path: Path) -> str:
        """Calculate file hash for change detection"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    def _get_name(self, node) -> str:
        """Extract name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)
    
    def _save_index(self):
        """Save index to disk"""
        try:
            data = {
                "last_indexed": self.last_indexed.isoformat() if self.last_indexed else None,
                "files": self.files,
                "symbols": {
                    name: [s.to_dict() for s in symbols]
                    for name, symbols in self.symbols.items()
                }
            }
            
            with open(self.index_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Index saved to {self.index_file}")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def load_index(self) -> bool:
        """Load index from disk"""
        try:
            if not self.index_file.exists():
                return False
            
            with open(self.index_file, 'r') as f:
                data = json.load(f)
            
            self.files = data.get("files", {})
            self.last_indexed = datetime.fromisoformat(data["last_indexed"]) if data.get("last_indexed") else None
            
            # Reconstruct symbols
            self.symbols = {}
            for name, symbol_dicts in data.get("symbols", {}).items():
                self.symbols[name] = [Symbol(**s) for s in symbol_dicts]
            
            logger.info(f"Index loaded from {self.index_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading index: {e}")
            return False

# Global index instance
_index: Optional[CodeIndex] = None

def get_index(workspace_path: str = ".") -> CodeIndex:
    """Get or create the global code index"""
    global _index
    if _index is None:
        _index = CodeIndex(workspace_path)
        _index.load_index()
    return _index

def rebuild_index(workspace_path: str = ".", force: bool = False) -> Dict[str, Any]:
    """Rebuild the code index"""
    index = get_index(workspace_path)
    return index.build_index(force=force)
