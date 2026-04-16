"""
Unit tests for preprocessor module.
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.core.preprocessor import preprocess_file, preprocess_source


class TestPreprocessor:
    """Test cases for preprocessor functions."""
    
    def test_preprocess_source_valid(self):
        """Test preprocessing valid Python source."""
        source = "def hello():\n    print('world')"
        tokens = preprocess_source(source)
        
        # Should contain normalized tokens
        assert "def" in tokens
        assert "FUNC" in tokens  # Function name
        assert "print" in tokens
        assert "STR" in tokens   # String literal
    
    def test_preprocess_source_empty(self):
        """Test preprocessing empty source."""
        tokens = preprocess_source("")
        assert tokens == []
    
    def test_preprocess_source_invalid(self):
        """Test preprocessing invalid input."""
        with pytest.raises(ValueError, match="source must be string"):
            preprocess_source(123)
        
        with pytest.raises(ValueError, match="source must be string"):
            preprocess_source(None)
    
    def test_preprocess_file_valid(self):
        """Test preprocessing valid Python file."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def test():\n    x = 1\n    return x")
            temp_path = f.name
        
        try:
            tokens = preprocess_file(temp_path)
            assert "def" in tokens
            assert "FUNC" in tokens
            assert "VAR" in tokens  # Variable x
            assert "NUM" in tokens  # Number 1
        finally:
            os.unlink(temp_path)
    
    def test_preprocess_file_not_found(self):
        """Test preprocessing non-existent file."""
        with pytest.raises(FileNotFoundError):
            preprocess_file("nonexistent.py")
    
    def test_preprocess_file_invalid_path(self):
        """Test preprocessing with invalid path type."""
        with pytest.raises(ValueError, match="Cannot read file"):
            preprocess_file(123)  # Invalid path type
    
    def test_normalization_rules(self):
        """Test token normalization rules."""
        source = """
        def my_func(x, y):
            if x > 0:
                return "hello" + str(y)
            else:
                print(len("test"))
        """
        
        tokens = preprocess_source(source)
        
        # Keywords
        assert "def" in tokens
        assert "if" in tokens
        assert "else" in tokens
        assert "return" in tokens
        
        # Built-ins
        assert "print" in tokens
        assert "len" in tokens
        assert "str" in tokens
        
        # Literals
        assert "STR" in tokens
        assert "NUM" in tokens
        
        # Names
        assert "FUNC" in tokens  # my_func
        assert "VAR" in tokens   # x, y
    
    def test_malformed_code(self):
        """Test preprocessing malformed Python code."""
        # This should not crash, but may produce partial tokens
        source = "def broken syntax {{{"
        tokens = preprocess_source(source)
        
        # Should still extract some valid tokens
        assert isinstance(tokens, list)
        # May be empty or partial due to tokenization errors