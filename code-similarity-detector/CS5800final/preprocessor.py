import tokenize
import io
import keyword
from pathlib import Path

# Public API
def preprocess_file(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8", errors="replace")
    return _tokenize_and_normalize(source)

def preprocess_source(source: str) -> list[str]:
    # Same as preprocess_file but accepts raw source code as a string
    return _tokenize_and_normalize(source)

# Internal helpers
# Token types we want to keep in the output stream
_KEEP = {
    tokenize.OP,
    tokenize.NAME,
    tokenize.NUMBER,
    tokenize.STRING,
}

# Python built-in functions (treated as BUILTIN, not VAR/FUNC)
_BUILTINS = frozenset(dir(__builtins__)) if isinstance(__builtins__, dict) \
            else frozenset(dir(__builtins__))

def _tokenize_and_normalize(source: str) -> list[str]:
    # Python keywords -> kept as-is (if, for, def, class, return, ...)
    # Built-in names -> kept as-is (print, len, range, ...)
    # Any other NAME that immediately follows 'def' or is used as a function call -> FUNC
    # Everything else -> VAR
    tokens: list[str] = []

    try:
        gen = tokenize.generate_tokens(io.StringIO(source).readline)
        raw = list(gen)
    except tokenize.TokenError:
        # Best-effort: tokenize whatever we got before the error
        raw = _partial_tokenize(source)

    # First pass: collect (type, string) pairs we care about
    filtered = [(t.type, t.string) for t in raw if t.type in _KEEP]

    # Second pass: normalize
    prev_string = ""
    # Track which positions are function definitions or calls
    # Look-ahead scan first to mark FUNC positions
    func_positions: set[int] = set()
    for i, (ttype, tstr) in enumerate(filtered):
        if ttype == tokenize.NAME:
            if prev_string == "def":
                func_positions.add(i)
            elif i + 1 < len(filtered) and filtered[i + 1][1] == "(":
                func_positions.add(i)
        prev_string = tstr

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

    return tokens

def _partial_tokenize(source: str) -> list:
    #Tokenize line-by-line, skipping lines that cause errors
    import tokenize as tk
    result = []
    lines = source.splitlines(keepends=True)
    for line in lines:
        try:
            toks = list(tk.generate_tokens(io.StringIO(line).readline))
            result.extend(toks)
        except tk.TokenError:
            pass
    return result