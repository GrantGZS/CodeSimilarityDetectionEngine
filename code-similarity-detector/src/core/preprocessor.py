"""
Unified Python code preprocessor.
Uses tokenization from CS5800final with enhanced robustness.
"""

import tokenize
import io
import keyword
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

# Token types to keep
_KEEP = {
    tokenize.OP,
    tokenize.NAME,
    tokenize.NUMBER,
    tokenize.STRING,
}

# Built-in functions and types
_BUILTINS = frozenset(dir(__builtins__)) if isinstance(__builtins__, dict) \
            else frozenset(dir(__builtins__))


def preprocess_file(path: Path) -> List[str]:
    """
    Preprocess Python file into normalized tokens.
    
    Args:
        path: Path to Python source file
    
    Returns:
        List of normalized token strings
    
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file is not valid Python or cannot be read
    """
    if not isinstance(path, Path):
        path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        logger.info(f"Read {len(source)} characters from {path}")
        return _tokenize_and_normalize(source)
    except IOError as e:
        logger.error(f"Cannot read file {path}: {e}")
        raise ValueError(f"Cannot read file {path}: {e}")


def preprocess_source(source: str) -> List[str]:
    """
    Preprocess Python source code (string) into normalized tokens.
    
    Args:
        source: Python source code as string
    
    Returns:
        List of normalized token strings
    
    Raises:
        ValueError: If source is invalid
    """
    if not isinstance(source, str):
        raise ValueError(f"source must be string, got {type(source)}")
    
    if len(source) == 0:
        logger.warning("Empty source code provided")
        return []
    
    logger.info(f"Preprocessing {len(source)} characters of source code")
    return _tokenize_and_normalize(source)


def _tokenize_and_normalize(source: str) -> List[str]:
    """
    Internal: tokenize and normalize Python source code.
    
    Normalization rules:
    - NUMBER tokens → "NUM"
    - STRING tokens → "STR"
    - Keywords (if, for, def, ...) → kept as-is
    - Built-ins (print, len, ...) → kept as-is
    - Names after 'def' or followed by '(' → "FUNC"
    - Other names → "VAR"
    - Operators → kept as-is
    
    Args:
        source: Python source code
    
    Returns:
        List of normalized tokens
    """
    tokens: List[str] = []
    
    try:
        gen = tokenize.generate_tokens(io.StringIO(source).readline)
        raw = list(gen)
        logger.debug(f"Tokenized into {len(raw)} raw tokens")
    except tokenize.TokenError as e:
        logger.warning(f"Tokenization error: {e}, attempting partial recovery")
        # Best-effort: tokenize whatever we got before the error
        raw = _partial_tokenize(source)
    
    # First pass: filter relevant tokens
    filtered = [(t.type, t.string) for t in raw if t.type in _KEEP]
    logger.debug(f"Filtered to {len(filtered)} relevant tokens")
    
    # Second pass: mark function positions (look-ahead scan)
    func_positions: set = set()
    prev_string = ""
    for i, (ttype, tstr) in enumerate(filtered):
        if ttype == tokenize.NAME:
            if prev_string == "def":
                func_positions.add(i)
            elif i + 1 < len(filtered) and filtered[i + 1][1] == "(":
                func_positions.add(i)
        prev_string = tstr
    
    logger.debug(f"Marked {len(func_positions)} function positions")
    
    # Third pass: normalize tokens
    for i, (ttype, tstr) in enumerate(filtered):
        if ttype == tokenize.NUMBER:
            tokens.append("NUM")
        elif ttype == tokenize.STRING:
            tokens.append("STR")
        elif ttype == tokenize.NAME:
            if keyword.iskeyword(tstr) or keyword.issoftkeyword(tstr):
                tokens.append(tstr)
            elif tstr in _BUILTINS:
                tokens.append(tstr)
            elif i in func_positions:
                tokens.append("FUNC")
            else:
                tokens.append("VAR")
        else:
            tokens.append(tstr)
    
    logger.info(f"Normalized to {len(tokens)} tokens")
    return tokens


def _partial_tokenize(source: str) -> list:
    """
    Best-effort line-by-line tokenization when full tokenization fails.
    
    Args:
        source: Python source code
    
    Returns:
        List of token objects (partial)
    """
    import tokenize as tk
    
    result = []
    lines = source.splitlines(keepends=True)
    
    for line_no, line in enumerate(lines, 1):
        try:
            toks = list(tk.generate_tokens(io.StringIO(line).readline))
            result.extend(toks)
        except tk.TokenError:
            logger.warning(f"Skipping line {line_no} due to tokenization error")
            # Skip malformed line
            pass
    
    logger.warning(f"Partial tokenization recovered {len(result)} tokens from {len(lines)} lines")
    return result