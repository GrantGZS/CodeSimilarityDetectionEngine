"""
Unit tests for SimilarityEngine class.
"""

import pytest
from src.core.engine import SimilarityEngine


class TestSimilarityEngine:
    """Test cases for SimilarityEngine."""
    
    def test_init_valid(self):
        """Test valid initialization."""
        engine = SimilarityEngine(k=5, jaccard_weight=0.4, lcs_weight=0.6)
        assert engine.k == 5
        assert engine.jaccard_weight == 0.4
        assert engine.lcs_weight == 0.6
    
    def test_init_invalid_k(self):
        """Test invalid k value."""
        with pytest.raises(ValueError, match="k must be positive"):
            SimilarityEngine(k=0)
        
        with pytest.raises(ValueError, match="k must be positive"):
            SimilarityEngine(k=-1)
    
    def test_init_invalid_weights(self):
        """Test invalid weight values."""
        with pytest.raises(ValueError, match="weights must be in"):
            SimilarityEngine(jaccard_weight=-0.1)
        
        with pytest.raises(ValueError, match="weights must sum to 1.0"):
            SimilarityEngine(jaccard_weight=0.5, lcs_weight=0.5)
    
    def test_get_shingles_valid(self):
        """Test shingle generation."""
        engine = SimilarityEngine(k=3)
        tokens = ["def", "hello", "print", "world"]
        shingles = engine.get_shingles(tokens)
        expected = {("def", "hello", "print"), ("hello", "print", "world")}
        assert shingles == expected
    
    def test_get_shingles_invalid(self):
        """Test shingle generation with invalid input."""
        engine = SimilarityEngine()
        with pytest.raises(ValueError, match="tokens cannot be None"):
            engine.get_shingles(None)
        
        with pytest.raises(ValueError, match="tokens must be a list"):
            engine.get_shingles("not a list")
    
    def test_jaccard_similarity(self):
        """Test Jaccard similarity calculation."""
        engine = SimilarityEngine()
        
        # Identical sets
        set1 = {1, 2, 3}
        set2 = {1, 2, 3}
        assert engine.jaccard_similarity(set1, set2) == 1.0
        
        # Empty sets (should be 1.0)
        assert engine.jaccard_similarity(set(), set()) == 1.0
        
        # Disjoint sets
        set1 = {1, 2}
        set2 = {3, 4}
        assert engine.jaccard_similarity(set1, set2) == 0.0
        
        # Partial overlap
        set1 = {1, 2, 3}
        set2 = {2, 3, 4}
        assert engine.jaccard_similarity(set1, set2) == 0.5
    
    def test_similarity(self):
        """Test shingle-based similarity."""
        engine = SimilarityEngine(k=2)
        tokens1 = ["a", "b", "c"]
        tokens2 = ["a", "b", "d"]
        
        # Should have some overlap
        score = engine.similarity(tokens1, tokens2)
        assert 0.0 <= score <= 1.0
    
    def test_compute_lcs(self):
        """Test LCS similarity."""
        engine = SimilarityEngine()
        
        # Identical sequences
        tokens1 = ["a", "b", "c"]
        tokens2 = ["a", "b", "c"]
        assert engine.compute_lcs(tokens1, tokens2) == 1.0
        
        # Empty sequences
        assert engine.compute_lcs([], []) == 1.0
        
        # Completely different
        tokens1 = ["a", "b"]
        tokens2 = ["c", "d"]
        assert engine.compute_lcs(tokens1, tokens2) == 0.0
    
    def test_get_final_score(self):
        """Test combined similarity score."""
        engine = SimilarityEngine(jaccard_weight=0.5, lcs_weight=0.5)
        
        tokens1 = ["def", "func", "print"]
        tokens2 = ["def", "func", "print"]
        
        score = engine.get_final_score(tokens1, tokens2)
        assert 0.0 <= score <= 1.0
    
    def test_compare_detailed(self):
        """Test detailed comparison."""
        engine = SimilarityEngine()
        tokens1 = ["a", "b"]
        tokens2 = ["a", "c"]
        
        result = engine.compare_detailed(tokens1, tokens2)
        
        required_keys = [
            "jaccard_similarity", "lcs_similarity", "final_similarity",
            "longest_matching_segment", "token_counts", "shingle_counts"
        ]
        
        for key in required_keys:
            assert key in result