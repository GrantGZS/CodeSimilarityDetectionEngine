"""
Unified Similarity Engine combining Jaccard + LCS algorithms.
- Best preprocessing logic from CS5800final/preprocessor.py
- Optimized LCS from CS5800final/lcs.py
- Robust error handling across both versions
"""

import logging
from typing import Tuple, List, Set, Dict, Any
from .similarity import jaccard, build_shingles, shingle_similarity
from .lcs import lcs_length, lcs_similarity, longest_matching_segment

logger = logging.getLogger(__name__)


class SimilarityEngine:
    """
    Unified code similarity detector using multiple algorithms.
    
    Combines:
    - Jaccard similarity (40% weight) - good for superficial similarity
    - LCS similarity (60% weight) - captures structural similarity
    
    Attributes:
        k: Shingle length (default 5)
        jaccard_weight: Weight for Jaccard score (default 0.4)
        lcs_weight: Weight for LCS score (default 0.6)
    
    Raises:
        ValueError: If k <= 0 or weights don't sum to 1.0
    """
    
    def __init__(
        self,
        k: int = 5,
        jaccard_weight: float = 0.4,
        lcs_weight: float = 0.6
    ):
        """
        Initialize SimilarityEngine.
        
        Args:
            k: Shingle length (must be > 0)
            jaccard_weight: Weight for Jaccard similarity [0, 1]
            lcs_weight: Weight for LCS similarity [0, 1]
        
        Raises:
            ValueError: If parameters are invalid
        """
        if k <= 0:
            raise ValueError(f"k must be positive, got {k}")
        
        if not (0 <= jaccard_weight <= 1) or not (0 <= lcs_weight <= 1):
            raise ValueError(
                f"weights must be in [0, 1], got jaccard={jaccard_weight}, lcs={lcs_weight}"
            )
        
        total_weight = jaccard_weight + lcs_weight
        if abs(total_weight - 1.0) > 1e-6:
            raise ValueError(
                f"weights must sum to 1.0, got {total_weight} "
                f"(jaccard={jaccard_weight}, lcs={lcs_weight})"
            )
        
        self.k = k
        self.jaccard_weight = jaccard_weight
        self.lcs_weight = lcs_weight
        
        logger.info(
            f"SimilarityEngine initialized: k={k}, "
            f"jaccard_weight={jaccard_weight}, lcs_weight={lcs_weight}"
        )
    
    # ============ Shingle-based Methods ============
    
    def get_shingles(self, tokens: List[str]) -> Set[Tuple[str, ...]]:
        """
        Convert token list to set of k-grams (shingles).
        
        Args:
            tokens: List of token strings
        
        Returns:
            Set of k-length tuples
        
        Raises:
            ValueError: If tokens is None or not a list
        """
        if tokens is None:
            raise ValueError("tokens cannot be None")
        if not isinstance(tokens, list):
            raise ValueError(f"tokens must be a list, got {type(tokens)}")
        
        return build_shingles(tokens, self.k)
    
    def jaccard_similarity(self, shingles1: Set, shingles2: Set) -> float:
        """
        Calculate Jaccard similarity between two shingle sets.
        
        Args:
            shingles1: First shingle set
            shingles2: Second shingle set
        
        Returns:
            Similarity score in [0.0, 1.0]
        
        Raises:
            ValueError: If sets are None
        """
        return jaccard(shingles1, shingles2)
    
    def similarity(self, tokens1: List[str], tokens2: List[str]) -> float:
        """
        Compute Jaccard similarity using shingles.
        
        Args:
            tokens1: First token list
            tokens2: Second token list
        
        Returns:
            Similarity score in [0.0, 1.0]
        
        Raises:
            ValueError: If inputs are invalid
        """
        if tokens1 is None or tokens2 is None:
            raise ValueError("token lists cannot be None")
        
        return shingle_similarity(tokens1, tokens2, self.k)
    
    # ============ LCS-based Methods ============
    
    def compute_lcs(self, tokens_a: List[str], tokens_b: List[str]) -> float:
        """
        Compute normalized LCS similarity (optimized O(min(m,n)) space).
        
        Args:
            tokens_a: First token list
            tokens_b: Second token list
        
        Returns:
            Normalized LCS score in [0.0, 1.0]
        
        Raises:
            ValueError: If inputs are invalid
        """
        if tokens_a is None or tokens_b is None:
            raise ValueError("token lists cannot be None")
        
        return lcs_similarity(tokens_a, tokens_b)
    
    def get_lcs_length(self, tokens_a: List[str], tokens_b: List[str]) -> int:
        """
        Get raw LCS length (for debugging/analysis).
        
        Args:
            tokens_a: First token list
            tokens_b: Second token list
        
        Returns:
            LCS length
        
        Raises:
            ValueError: If inputs are invalid
        """
        if tokens_a is None or tokens_b is None:
            raise ValueError("token lists cannot be None")
        
        return lcs_length(tokens_a, tokens_b)
    
    def get_longest_match(
        self, tokens_a: List[str], tokens_b: List[str]
    ) -> Dict[str, Any]:
        """
        Find longest contiguous matching segment.
        
        Args:
            tokens_a: First token list
            tokens_b: Second token list
        
        Returns:
            Dict with keys: length, start_a, start_b, segment_a, segment_b
        
        Raises:
            ValueError: If inputs are invalid
        """
        if tokens_a is None or tokens_b is None:
            raise ValueError("token lists cannot be None")
        
        length, start_a, start_b = longest_matching_segment(tokens_a, tokens_b)
        
        segment_a = tokens_a[start_a : start_a + length] if length > 0 else []
        segment_b = tokens_b[start_b : start_b + length] if length > 0 else []
        
        return {
            "length": length,
            "start_a": start_a,
            "start_b": start_b,
            "segment_a": segment_a,
            "segment_b": segment_b,
        }
    
    # ============ Unified Scoring ============
    
    def get_final_score(self, tokens1: List[str], tokens2: List[str]) -> float:
        """
        Compute weighted similarity score.
        
        Combines Jaccard (superficial) + LCS (structural) similarities.
        
        Args:
            tokens1: First token list
            tokens2: Second token list
        
        Returns:
            Combined score in [0.0, 1.0]
        
        Raises:
            ValueError: If inputs are invalid
        """
        if tokens1 is None or tokens2 is None:
            raise ValueError("token lists cannot be None")
        
        j_score = self.similarity(tokens1, tokens2)
        l_score = self.compute_lcs(tokens1, tokens2)
        
        final_score = (self.jaccard_weight * j_score) + (self.lcs_weight * l_score)
        
        logger.debug(
            f"Final score: {final_score:.4f} "
            f"(Jaccard={j_score:.4f}, LCS={l_score:.4f})"
        )
        
        return final_score
    
    def compare_detailed(
        self, tokens1: List[str], tokens2: List[str]
    ) -> Dict[str, Any]:
        """
        Comprehensive comparison with all metrics.
        
        Args:
            tokens1: First token list
            tokens2: Second token list
        
        Returns:
            Dictionary with all similarity metrics
        
        Raises:
            ValueError: If inputs are invalid
        """
        if tokens1 is None or tokens2 is None:
            raise ValueError("token lists cannot be None")
        
        shingles1 = self.get_shingles(tokens1)
        shingles2 = self.get_shingles(tokens2)
        
        j_score = self.jaccard_similarity(shingles1, shingles2)
        l_score = self.compute_lcs(tokens1, tokens2)
        final_score = self.get_final_score(tokens1, tokens2)
        longest_match = self.get_longest_match(tokens1, tokens2)
        
        return {
            "jaccard_similarity": j_score,
            "lcs_similarity": l_score,
            "final_similarity": final_score,
            "longest_matching_segment": longest_match,
            "token_counts": {
                "tokens1": len(tokens1),
                "tokens2": len(tokens2),
            },
            "shingle_counts": {
                "shingles1": len(shingles1),
                "shingles2": len(shingles2),
                "common_shingles": len(shingles1 & shingles2),
            },
        }