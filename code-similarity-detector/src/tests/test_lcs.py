"""
Unit tests for LCS module.
"""

import pytest
from src.core.lcs import lcs_length, lcs_similarity, longest_matching_segment, extract_segment_tokens


class TestLCS:
    """Test cases for LCS functions."""
    
    def test_lcs_length_identical(self):
        """Test LCS length with identical sequences."""
        a = ["a", "b", "c"]
        b = ["a", "b", "c"]
        assert lcs_length(a, b) == 3
    
    def test_lcs_length_empty(self):
        """Test LCS length with empty sequences."""
        assert lcs_length([], []) == 0
        assert lcs_length([], ["a"]) == 0
        assert lcs_length(["a"], []) == 0
    
    def test_lcs_length_partial(self):
        """Test LCS length with partial overlap."""
        a = ["a", "b", "c", "d"]
        b = ["b", "c", "d", "e"]
        # LCS should be ["b", "c", "d"] (length 3)
        assert lcs_length(a, b) == 3
    
    def test_lcs_length_no_overlap(self):
        """Test LCS length with no overlap."""
        a = ["a", "b"]
        b = ["c", "d"]
        assert lcs_length(a, b) == 0
    
    def test_lcs_length_invalid(self):
        """Test LCS length with invalid input."""
        with pytest.raises(ValueError, match="token lists cannot be None"):
            lcs_length(None, ["a"])
        
        with pytest.raises(ValueError, match="token lists cannot be None"):
            lcs_length(["a"], None)
        
        with pytest.raises(ValueError, match="inputs must be lists"):
            lcs_length("not a list", ["a"])
        
        with pytest.raises(ValueError, match="all elements in a must be strings"):
            lcs_length([1, 2], ["a", "b"])
    
    def test_lcs_similarity_identical(self):
        """Test LCS similarity with identical sequences."""
        a = ["a", "b", "c"]
        b = ["a", "b", "c"]
        assert lcs_similarity(a, b) == 1.0
    
    def test_lcs_similarity_empty(self):
        """Test LCS similarity with empty sequences (should be 1.0)."""
        assert lcs_similarity([], []) == 1.0
    
    def test_lcs_similarity_one_empty(self):
        """Test LCS similarity with one empty sequence."""
        assert lcs_similarity([], ["a"]) == 0.0
        assert lcs_similarity(["a"], []) == 0.0
    
    def test_lcs_similarity_partial(self):
        """Test LCS similarity with partial overlap."""
        a = ["a", "b", "c"]
        b = ["a", "x", "c"]
        # LCS is ["a", "c"] (length 2), max len is 3, so 2/3
        assert lcs_similarity(a, b) == 2/3
    
    def test_lcs_similarity_invalid(self):
        """Test LCS similarity with invalid input."""
        with pytest.raises(ValueError, match="token lists cannot be None"):
            lcs_similarity(None, ["a"])
    
    def test_longest_matching_segment_identical(self):
        """Test longest matching segment with identical sequences."""
        a = ["a", "b", "c"]
        b = ["a", "b", "c"]
        length, start_a, start_b = longest_matching_segment(a, b)
        assert length == 3
        assert start_a == 0
        assert start_b == 0
    
    def test_longest_matching_segment_empty(self):
        """Test longest matching segment with empty sequences."""
        length, start_a, start_b = longest_matching_segment([], [])
        assert length == 0
        assert start_a == 0
        assert start_b == 0
    
    def test_longest_matching_segment_partial(self):
        """Test longest matching segment with partial overlap."""
        a = ["x", "a", "b", "c", "y"]
        b = ["z", "a", "b", "c", "w"]
        length, start_a, start_b = longest_matching_segment(a, b)
        assert length == 3  # "a", "b", "c"
        assert start_a == 1
        assert start_b == 1
    
    def test_longest_matching_segment_no_match(self):
        """Test longest matching segment with no contiguous match."""
        a = ["a", "x", "b"]
        b = ["a", "y", "b"]
        length, start_a, start_b = longest_matching_segment(a, b)
        assert length == 1  # Single "a" or "b"
    
    def test_longest_matching_segment_invalid(self):
        """Test longest matching segment with invalid input."""
        with pytest.raises(ValueError, match="token lists cannot be None"):
            longest_matching_segment(None, ["a"])
    
    def test_extract_segment_tokens_valid(self):
        """Test segment extraction with valid input."""
        tokens = ["a", "b", "c", "d"]
        segment = extract_segment_tokens(tokens, 1, 2)
        assert segment == ["b", "c"]
    
    def test_extract_segment_tokens_empty(self):
        """Test segment extraction with zero length."""
        tokens = ["a", "b", "c"]
        segment = extract_segment_tokens(tokens, 1, 0)
        assert segment == []
    
    def test_extract_segment_tokens_invalid(self):
        """Test segment extraction with invalid input."""
        with pytest.raises(ValueError, match="tokens cannot be None"):
            extract_segment_tokens(None, 0, 1)
        
        with pytest.raises(ValueError, match="start and length must be non-negative"):
            extract_segment_tokens(["a"], -1, 1)
        
        with pytest.raises(ValueError, match="segment out of bounds"):
            extract_segment_tokens(["a"], 0, 2)