"""
Unified Jaccard similarity and shingle-based algorithms.
Combines best practices from src/engine.py and CS5800final/shingling.py
"""

import logging
from typing import Set, Tuple, List

logger = logging.getLogger(__name__)


def build_shingles(tokens: List[str], k: int = 5) -> Set[Tuple[str, ...]]:
    """
    Build k-grams (shingles) from token list.
    
    Args:
        tokens: List of token strings
        k: Shingle length (must be > 0)
    
    Returns:
        Set of k-length tuples
    
    Raises:
        ValueError: If inputs are invalid
    """
    if tokens is None:
        raise ValueError("tokens cannot be None")
    if k <= 0:
        raise ValueError(f"k must be positive, got {k}")
    
    if len(tokens) == 0:
        return set()
    
    if len(tokens) < k:
        logger.debug(
            f"tokens length ({len(tokens)}) < k ({k}), returning empty shingle set"
        )
        return set()
    
    shingles = {tuple(tokens[i : i + k]) for i in range(len(tokens) - k + 1)}
    logger.debug(f"Built {len(shingles)} shingles from {len(tokens)} tokens (k={k})")
    
    return shingles


def jaccard(set_a: Set, set_b: Set) -> float:
    """
    Compute Jaccard similarity coefficient between two sets.
    
    Formula: |A ∩ B| / |A ∪ B|
    
    Args:
        set_a: First set
        set_b: Second set
    
    Returns:
        Jaccard similarity in [0.0, 1.0]:
        - 1.0: identical sets (including both empty)
        - 0.0: completely disjoint
    
    Raises:
        ValueError: If sets are None
    """
    if set_a is None or set_b is None:
        raise ValueError("sets cannot be None")
    
    # Special case: both empty → identical → 1.0
    if not set_a and not set_b:
        return 1.0
    
    # One empty, one non-empty → disjoint → 0.0
    if not set_a or not set_b:
        return 0.0
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    if union == 0:  # Safety check
        return 0.0
    
    similarity = intersection / union
    logger.debug(
        f"Jaccard: {similarity:.4f} (intersection={intersection}, union={union})"
    )
    
    return similarity


def shingle_similarity(tokens_a: List[str], tokens_b: List[str], k: int = 5) -> float:
    """
    Compute Jaccard similarity using shingles.
    
    Args:
        tokens_a: First token list
        tokens_b: Second token list
        k: Shingle length (default 5)
    
    Returns:
        Similarity score in [0.0, 1.0]
    
    Raises:
        ValueError: If inputs are invalid
    """
    if tokens_a is None or tokens_b is None:
        raise ValueError("token lists cannot be None")
    
    shingles_a = build_shingles(tokens_a, k)
    shingles_b = build_shingles(tokens_b, k)
    
    return jaccard(shingles_a, shingles_b)