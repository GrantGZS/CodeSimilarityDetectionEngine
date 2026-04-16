"""
Unit tests for similarity module.
"""

import pytest
from src.core.similarity import build_shingles, jaccard, shingle_similarity


class TestSimilarity:
    """Test cases for similarity functions."""
    
    def test_build_shingles_valid(self):
        """Test shingle building with valid input."""
        tokens = ["a", "b", "c", "d"]
        shingles = build_shingles(tokens, k=2)
        expected = {("a", "b"), ("b", "c"), ("c", "d")}
        assert shingles == expected
    
    def test_build_shingles_empty(self):
        """Test shingle building with empty tokens."""
        assert build_shingles([], k=2) == set()
    
    def test_build_shingles_short(self):
        """Test shingle building when tokens shorter than k."""
        tokens = ["a", "b"]
        assert build_shingles(tokens, k=3) == set()
    
    def test_build_shingles_invalid(self):
        """Test shingle building with invalid input."""
        with pytest.raises(ValueError, match="tokens cannot be None"):
            build_shingles(None, k=2)
        
        with pytest.raises(ValueError, match="k must be positive"):
            build_shingles(["a", "b"], k=0)
        
        with pytest.raises(ValueError, match="k must be positive"):
            build_shingles(["a", "b"], k=-1)
    
    def test_jaccard_identical(self):
        """Test Jaccard with identical sets."""
        set1 = {1, 2, 3}
        set2 = {1, 2, 3}
        assert jaccard(set1, set2) == 1.0
    
    def test_jaccard_empty(self):
        """Test Jaccard with empty sets (should be 1.0)."""
        assert jaccard(set(), set()) == 1.0
    
    def test_jaccard_disjoint(self):
        """Test Jaccard with disjoint sets."""
        set1 = {1, 2}
        set2 = {3, 4}
        assert jaccard(set1, set2) == 0.0
    
    def test_jaccard_partial(self):
        """Test Jaccard with partial overlap."""
        set1 = {1, 2, 3}
        set2 = {2, 3, 4}
        assert jaccard(set1, set2) == 0.5
    
    def test_jaccard_invalid(self):
        """Test Jaccard with invalid input."""
        with pytest.raises(ValueError, match="sets cannot be None"):
            jaccard(None, {1, 2})
        
        with pytest.raises(ValueError, match="sets cannot be None"):
            jaccard({1, 2}, None)
    
    def test_shingle_similarity_identical(self):
        """Test shingle similarity with identical tokens."""
        tokens1 = ["a", "b", "c"]
        tokens2 = ["a", "b", "c"]
        score = shingle_similarity(tokens1, tokens2, k=2)
        assert score == 1.0
    
    def test_shingle_similarity_different(self):
        """Test shingle similarity with different tokens."""
        tokens1 = ["a", "b", "c"]
        tokens2 = ["x", "y", "z"]
        score = shingle_similarity(tokens1, tokens2, k=2)
        assert score == 0.0
    
    def test_shingle_similarity_partial(self):
        """Test shingle similarity with partial overlap."""
        tokens1 = ["a", "b", "c", "d"]
        tokens2 = ["b", "c", "d", "e"]
        score = shingle_similarity(tokens1, tokens2, k=2)
        # Should have some overlap: ("b","c"), ("c","d")
        assert 0.0 < score < 1.0
    
    def test_shingle_similarity_invalid(self):
        """Test shingle similarity with invalid input."""
        with pytest.raises(ValueError, match="token lists cannot be None"):
            shingle_similarity(None, ["a", "b"])
        
        with pytest.raises(ValueError, match="token lists cannot be None"):
            shingle_similarity(["a", "b"], None)