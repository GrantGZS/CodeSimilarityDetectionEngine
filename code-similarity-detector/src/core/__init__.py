"""
Core module for code similarity detection.

This module provides the main APIs for:
- Preprocessing Python code into tokens
- Computing similarity using Jaccard and LCS algorithms
- Unified similarity engine combining multiple metrics
"""

from .engine import SimilarityEngine
from .preprocessor import preprocess_file, preprocess_source
from .similarity import build_shingles, jaccard, shingle_similarity
from .lcs import lcs_length, lcs_similarity, longest_matching_segment, extract_segment_tokens

__all__ = [
    # Main engine
    "SimilarityEngine",
    
    # Preprocessing
    "preprocess_file",
    "preprocess_source",
    
    # Similarity algorithms
    "build_shingles",
    "jaccard",
    "shingle_similarity",
    
    # LCS algorithms
    "lcs_length",
    "lcs_similarity",
    "longest_matching_segment",
    "extract_segment_tokens",
]