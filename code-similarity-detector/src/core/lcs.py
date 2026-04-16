"""
Unified LCS (Longest Common Subsequence) implementation.
- Optimized space complexity O(min(m,n)) vs O(m*n)
- Combines best practices from both versions
"""

import logging
from typing import Tuple, List

logger = logging.getLogger(__name__)


def lcs_length(a: List[str], b: List[str]) -> int:
    """
    Compute LCS length using space-optimized DP.
    
    Time complexity: O(m*n)
    Space complexity: O(min(m,n)) using two-row rolling array
    
    Args:
        a: First token list
        b: Second token list
    
    Returns:
        Length of longest common subsequence
    
    Raises:
        ValueError: If inputs are invalid
    """
    if a is None or b is None:
        raise ValueError("token lists cannot be None")
    
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("inputs must be lists")
    
    n, m = len(a), len(b)
    
    # Handle empty cases
    if n == 0 or m == 0:
        return 0
    
    # Validate token types
    if not all(isinstance(t, str) for t in a):
        raise ValueError("all elements in a must be strings")
    if not all(isinstance(t, str) for t in b):
        raise ValueError("all elements in b must be strings")
    
    # Optimize: make b the shorter sequence (better cache locality)
    if n < m:
        a, b = b, a
        n, m = m, n
    
    # Two-row DP: only keep current and previous rows
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        # Swap rows
        prev, curr = curr, [0] * (m + 1)
    
    result = prev[m]
    logger.debug(f"LCS length: {result} (a={n}, b={m})")
    
    return result


def lcs_similarity(a: List[str], b: List[str]) -> float:
    """
    Compute normalized LCS similarity score.
    
    Args:
        a: First token list
        b: Second token list
    
    Returns:
        Normalized LCS score in [0.0, 1.0]:
        - 1.0: identical or both empty
        - 0.0: completely disjoint
    
    Raises:
        ValueError: If inputs are invalid
    """
    if a is None or b is None:
        raise ValueError("token lists cannot be None")
    
    # Special case: both empty → identical → 1.0
    if not a and not b:
        return 1.0
    
    # One or both non-empty
    if not a or not b:
        return 0.0
    
    length = lcs_length(a, b)
    max_len = max(len(a), len(b))
    
    if max_len == 0:  # Safety check
        return 0.0
    
    similarity = length / max_len
    logger.debug(f"LCS similarity: {similarity:.4f} (length={length}, max={max_len})")
    
    return similarity


def longest_matching_segment(a: List[str], b: List[str]) -> Tuple[int, int, int]:
    """
    Find longest contiguous matching segment (substring, not subsequence).
    
    Time complexity: O(m*n)
    Space complexity: O(min(m,n))
    
    Args:
        a: First token list
        b: Second token list
    
    Returns:
        Tuple of (length, start_a, start_b) where:
        - length: length of longest match
        - start_a: starting index in a
        - start_b: starting index in b
    
    Raises:
        ValueError: If inputs are invalid
    """
    if a is None or b is None:
        raise ValueError("token lists cannot be None")
    
    if not isinstance(a, list) or not isinstance(b, list):
        raise ValueError("inputs must be lists")
    
    n, m = len(a), len(b)
    
    if n == 0 or m == 0:
        return (0, 0, 0)
    
    # Optimize: make b the column dimension
    swapped = False
    if n < m:
        a, b = b, a
        n, m = m, n
        swapped = True
    
    best_len = 0
    best_end_a = 0
    best_end_b = 0
    
    prev = [0] * (m + 1)
    curr = [0] * (m + 1)
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
                if curr[j] > best_len:
                    best_len = curr[j]
                    best_end_a = i
                    best_end_b = j
            else:
                curr[j] = 0
        prev, curr = curr, [0] * (m + 1)
    
    start_a = best_end_a - best_len
    start_b = best_end_b - best_len
    
    # Swap back to refer to original sequences
    if swapped:
        start_a, start_b = start_b, start_a
    
    logger.debug(
        f"Longest match: {best_len} tokens at a[{start_a}:{start_a + best_len}], "
        f"b[{start_b}:{start_b + best_len}]"
    )
    
    return (best_len, start_a, start_b)


def extract_segment_tokens(tokens: List[str], start: int, length: int) -> List[str]:
    """
    Extract contiguous segment from token list.
    
    Args:
        tokens: Token list
        start: Starting index
        length: Segment length
    
    Returns:
        Extracted segment
    
    Raises:
        ValueError: If indices are invalid
    """
    if tokens is None:
        raise ValueError("tokens cannot be None")
    if start < 0 or length < 0:
        raise ValueError(
            f"start and length must be non-negative (start={start}, length={length})"
        )
    if start + length > len(tokens):
        raise ValueError(
            f"segment out of bounds: start={start}, length={length}, "
            f"tokens has {len(tokens)} elements"
        )
    
    return tokens[start : start + length]