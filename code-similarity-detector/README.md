# Code Similarity Detection

A Python-based code similarity detection system using multiple algorithms to identify similar code patterns, detect plagiarism, and compare code implementations.

## Project Overview

This project implements a **Code Similarity Detector** that compares code snippets using two primary algorithms:

1. **Jaccard Similarity** - Shingle-based approach using k-grams to find common token patterns
2. **Longest Common Subsequence (LCS)** - Sequence-based approach to find the longest matching token sequences

These algorithms work together to detect:
- **Identical code** - Exact code matches
- **Renamed variables** - Code with variable name changes but same logic
- **Structural changes** - Code with modified control flow or operations

## Project Structure

```
code-similarity-detector/
├── README.md                          # Project documentation
├── data/
│   └── mock_tokens/
│       └── sample_pairs.json         # Mock test data with token pairs
├── src/
│   ├── __init__.py                   # Package initializer
│   ├── engine.py                     # SimilarityEngine class implementation
│   └── preprocess_mock.py            # Mock preprocessing function
└── tests/
    └── test_engine.py                # Test script with comprehensive analysis
```

## Installation & Setup

### Prerequisites

- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd code-similarity-detector
   ```

2. **Verify the directory structure**
   ```bash
   ls -la
   ```

3. **Check that all required files exist**
   ```bash
   # Should see: data/, src/, tests/, README.md
   ls -la
   ```

## Usage

### Running the Test Suite

Execute the comprehensive test suite to see how the similarity algorithms perform:

```bash
python tests/test_engine.py
```

This will:
- Load test cases from `data/mock_tokens/sample_pairs.json`
- Initialize SimilarityEngine with k=3 (for 3-gram shingles)
- Calculate Jaccard, LCS, and Combined similarity scores
- Display results in a formatted table with performance analysis

### Example Output

```
Code Similarity Detection Test Results
================================================================================
Test Case                Jaccard         LCS             Combined       
--------------------------------------------------------------------------------
Identical code           1.0000          1.0000          1.0000         
Renamed variables        1.0000          1.0000          1.0000         
Structural changes       0.5556          0.4286          0.4921         
================================================================================
```

### Using the SimilarityEngine in Your Code

```python
from src.engine import SimilarityEngine

# Initialize with k=3 (3-grams/shingles)
engine = SimilarityEngine(k=3)

# Your token lists
tokens_file_a = ["DEF", "FUNC", "LPAREN", "VAR", "RPAREN", "COLON", "RETURN", "VAR"]
tokens_file_b = ["DEF", "FUNC", "LPAREN", "VAR", "RPAREN", "COLON", "RETURN", "VAR"]

# Calculate Jaccard similarity (shingle-based)
jaccard_score = engine.similarity(tokens_file_a, tokens_file_b)
print(f"Jaccard Similarity: {jaccard_score}")  # Output: 1.0

# Calculate LCS similarity (sequence-based)
lcs_score = engine.compute_lcs(tokens_file_a, tokens_file_b)
print(f"LCS Similarity: {lcs_score}")  # Output: 1.0

# Combined score (average of both)
combined = (jaccard_score + lcs_score) / 2
print(f"Combined Score: {combined}")  # Output: 1.0
```

### Using the Mock Preprocessing Function

For testing purposes, use the mock tokenizer to load test data:

```python
from src.preprocess_mock import mock_tokenize

# Load test case tokens
tokens_a, tokens_b = mock_tokenize('case_1_identical')

# Or other available cases:
# - 'case_1_identical'
# - 'case_2_renamed'
# - 'case_3_structural_change'
```

## Component Overview

### SimilarityEngine (`src/engine.py`)

The main class for computing code similarity.

**Constructor:**
- `__init__(self, k)` - Initialize with shingle size k

**Methods:**

1. **`get_shingles(tokens)`** - Converts tokens to k-grams
   - Input: List of tokens
   - Output: Set of tuples (shingles)

2. **`jaccard_similarity(shingles1, shingles2)`** - Compute Jaccard similarity
   - Formula: |A ∩ B| / |A ∪ B|
   - Range: 0.0 to 1.0
   - Better for: Detecting identical and near-identical code

3. **`compute_lcs(tokens_a, tokens_b)`** - Compute normalized LCS similarity
   - Uses dynamic programming
   - Normalized by max length of input sequences
   - Range: 0.0 to 1.0
   - Better for: Detecting sequential similarities

4. **`similarity(tokens1, tokens2)`** - Unified similarity computation
   - Combines get_shingles and jaccard_similarity
   - Returns Jaccard score

### Mock Preprocessing (`src/preprocess_mock.py`)

Temporary replacement for real preprocessing pipeline.

**Function:**
- `mock_tokenize(file_path)` - Load tokens from JSON test data
  - Parameter: Case name (e.g., 'case_1_identical')
  - Returns: Tuple of (tokens_a, tokens_b)

## Test Data

Test cases are stored in `data/mock_tokens/sample_pairs.json`:

- **case_1_identical**: Identical code (same tokens)
- **case_2_renamed**: Renamed variables (same structure, different identifiers)
- **case_3_structural_change**: Changed control flow (FOR vs WHILE loop)

## Algorithm Details

### Jaccard Similarity (Shingle-based)

1. Convert token sequences to k-gram shingles
2. Find intersection and union of shingle sets
3. Calculate: similarity = |intersection| / |union|

**Advantages:**
- Fast computation
- Good for detecting exact matches
- Resistant to small changes

**Limitations:**
- Doesn't consider token order
- Sensitive to large structural changes

### LCS Similarity (Sequence-based)

1. Build dynamic programming table for longest common subsequence
2. Find length of longest matching token sequence
3. Normalize by maximum sequence length

**Advantages:**
- Considers token order
- Good for detecting structural similarities
- Handles insertions and deletions

**Limitations:**
- O(m*n) time complexity
- May miss some pattern similarities

## Performance Insights

From test results:

| Scenario | Jaccard | LCS | Best Use |
|----------|---------|-----|----------|
| Identical Code | Very High (≈1.0) | Very High (≈1.0) | Both excellent |
| Renamed Variables | High | High | Both detect well |
| Structural Changes | Moderate | Lower | May need combined approach |

The **combined score** (average of both) provides a balanced assessment of similarity.

## Future Enhancements

- Implement real preprocessing pipeline (tokenization from source code)
- Add more similarity metrics (MinHash, SimHash)
- Support multiple programming languages
- Add weighted scoring for different token types
- Implement database storage for comparison results

## Team Members

Work on this project together by:

1. Running tests locally: `python tests/test_engine.py`
2. Modifying test cases in `data/mock_tokens/sample_pairs.json`
3. Extending the SimilarityEngine with new algorithms
4. Creating real preprocessing functions in `src/preprocess_mock.py`

## License

This project is part of CS5800 Final Project.

## Questions or Issues?

Refer to the code comments in `src/engine.py` for algorithm implementation details, or check the test output for performance analysis.
