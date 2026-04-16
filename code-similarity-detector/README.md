# Code Similarity Detection System

## 📖 Project Overview

This is a Python-based code similarity detection system designed to detect plagiarism in programming assignments. The system combines Jaccard similarity (using k-shingles) and Longest Common Subsequence (LCS) algorithms to provide accurate and efficient similarity calculations.

## ✨ Key Features

- **Multi-Algorithm Fusion**: Combines Jaccard and LCS algorithms for improved accuracy
- **Intelligent Preprocessing**: Automatically parses Python code into meaningful tokens
- **Batch Detection**: Supports pairwise comparisons for large file sets
- **Detailed Reporting**: Generates ranked lists of suspicious file pairs and performance statistics
- **Test Data Generation**: Automatically creates mutated test files for system evaluation
- **Performance Metrics**: Provides Precision@20, Recall@20, and other evaluation metrics

## 🚀 Quick Start

### 1. System Requirements

- Python 3.7+
- Dependencies: `astor` (for code parsing)

### 2. Install Dependencies

```bash
cd /Users/kewu/Desktop/CS5800FinalProjectCodeSimilarityDetection/code-similarity-detector
pip install astor
```

### 3. Verify Installation

```bash
python -c "from src.core import SimilarityEngine; print('✅ Installation successful')"
```

## 📁 Project Structure

```
code-similarity-detector/
├── src/
│   ├── core/
│   │   ├── __init__.py          # Core module exports
│   │   ├── engine.py            # SimilarityEngine class
│   │   ├── preprocessor.py      # Code preprocessing and tokenization
│   │   ├── similarity.py        # Jaccard and Shingle algorithms
│   │   └── lcs.py               # LCS algorithm implementation
│   ├── tests/                   # Unit tests
│   │   ├── test_engine.py       # Engine tests
│   │   ├── test_preprocessor.py # Preprocessing tests
│   │   ├── test_similarity.py   # Similarity algorithm tests
│   │   └── test_lcs.py          # LCS algorithm tests
│   └── utils/
│       └── logger.py            # Logging utilities
├── submissions/                 # Test files directory (auto-generated)
├── ground_truth.json            # Ground truth file (auto-generated)
├── results.json                 # Detection results (auto-generated)
├── test_generator.py            # Test data generator
├── reporter.py                  # Similarity detection reporter
└── README.md                    # Project documentation
```

## 🛠️ Usage Guide

### Step 1: Generate Test Data

Run the test generator to create test files:

```bash
python test_generator.py
```

This will:
- Create the `submissions/` directory
- Generate 50 Python files based on 5 base templates with mutations
- Create `ground_truth.json` recording truly similar file pairs (225 pairs)

### Step 2: Run Similarity Detection

Execute the reporter for comprehensive analysis:

```bash
python reporter.py
```

This will:
- Perform pairwise comparisons on all files (1,225 comparisons)
- Generate Top 20 suspicious pairs (highest similarity)
- Generate Top 20 false positives (highest similarity among non-similar pairs)
- Calculate performance statistics (Precision@20, Recall@20)
- Save detailed results to `results.json`
- Print a formatted terminal report

### Step 3: View Results

#### Terminal Report Example

```
================================================================================
🎯 CODE SIMILARITY DETECTION REPORT
================================================================================

📊 STATISTICS:
   Total Comparisons: 1,225
   True Positives (Total): 225
   False Positives (Total): 1,000
   Total True Pairs (Ground Truth): 225

🎯 TOP 20 SUSPICIOUS PAIRS (Highest Similarity Overall):
   Precision: 100.0%
   Recall: 8.9%
   True Positives: 20/20
--------------------------------------------------------------------------------
Rank File 1          File 2          Similarity  Type
--------------------------------------------------------------------------------
1    test_0001.py     test_0002.py     0.8542     ✅ TP
2    test_0001.py     test_0003.py     0.8421     ✅ TP
...

❌ TOP 20 FALSE POSITIVES (Highest Similarity Among Non-Similar Pairs):
   False Positives: 20/20
--------------------------------------------------------------------------------
Rank File 1          File 2          Similarity
--------------------------------------------------------------------------------
1    test_0041.py     test_0001.py     0.1234
...
```

#### JSON Results File

`results.json` contains complete analysis:
- `all_comparisons`: All 1,225 comparison results
- `top_20_suspicious`: Top 20 suspicious pairs details
- `top_20_false_positives`: Top 20 false positive pairs details
- `statistics`: Performance metrics

## 🔧 API Usage Examples

### Basic Similarity Detection

```python
from src.core import SimilarityEngine, preprocess_file

# Create engine (k=5 for 5-gram shingles)
engine = SimilarityEngine(k=5)

# Preprocess Python files
tokens1 = preprocess_file("submissions/test_0001.py")
tokens2 = preprocess_file("submissions/test_0002.py")

# Calculate combined similarity
score = engine.get_final_score(tokens1, tokens2)
print(f"Similarity: {score:.4f}")  # 0.0-1.0 range
```

### Detailed Comparison Analysis

```python
# Get detailed comparison results
result = engine.compare_detailed(tokens1, tokens2)

print(f"Jaccard Similarity: {result['jaccard_similarity']:.4f}")
print(f"LCS Similarity: {result['lcs_similarity']:.4f}")
print(f"Combined Similarity: {result['final_similarity']:.4f}")
print(f"Longest Matching Segment: {result['longest_matching_segment']}")
```

### Using Individual Algorithms

```python
from src.core import jaccard, lcs_similarity, build_shingles

# Jaccard similarity calculation
shingles1 = build_shingles(tokens1, k=3)
shingles2 = build_shingles(tokens2, k=3)
jaccard_score = jaccard(shingles1, shingles2)

# LCS similarity calculation
lcs_score = lcs_similarity(tokens1, tokens2)

print(f"Jaccard: {jaccard_score:.4f}, LCS: {lcs_score:.4f}")
```

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
python -m pytest src/tests/ -v

# Run specific module tests
python -m pytest src/tests/test_engine.py -v
python -m pytest src/tests/test_preprocessor.py -v
```

### Performance Evaluation

Evaluate system performance using generated test data:

```bash
python reporter.py
```

Key metrics to check:
- **Precision@20**: Proportion of truly similar pairs in Top 20
- **Recall@20**: Proportion of detected true pairs out of total true pairs

## 📊 Algorithm Details

### SimilarityEngine

Core computation logic:

1. **Preprocessing**: Convert code to token sequences
2. **Jaccard Calculation**: Set-based similarity using k-shingles
3. **LCS Calculation**: Sequence-based longest common subsequence
4. **Weighted Fusion**: `final = jaccard_weight × jaccard + lcs_weight × lcs`

**Parameters**:
- `k`: Shingle size (default 5)
- `jaccard_weight`: Jaccard weight (default 0.5)
- `lcs_weight`: LCS weight (default 0.5)

### Preprocessing (preprocessor.py)

Converts Python source code to normalized token lists:

- **Preserves**: Keywords, operators, literals
- **Normalizes**: Variables → VAR, functions → FUNC, strings → STR, numbers → NUM
- **Removes**: Comments, whitespace, indentation differences

### Mutation Strategies (test_generator.py)

Code mutations applied when generating test files:

- **Variable Renaming**: Random variable name replacement
- **Indentation Changes**: Adjust code indentation
- **Dead Code Insertion**: Add non-functional code snippets
- **Function Reordering**: Rearrange function definitions

## 📈 Performance Insights

Based on test data analysis:

| Scenario | Jaccard | LCS | Combined Score | Detection Effectiveness |
|----------|---------|-----|----------------|------------------------|
| Identical Code | 1.000 | 1.000 | 1.000 | Perfect Detection |
| Variable Renaming | 1.000 | 1.000 | 1.000 | Perfect Detection |
| Structural Changes | 0.5-0.8 | 0.3-0.6 | 0.4-0.7 | Good Detection |
| Dissimilar Code | 0.0-0.2 | 0.0-0.1 | 0.0-0.15 | Correct Exclusion |

**Key Findings**:
- High accuracy in plagiarism detection
- Combined algorithms handle different types of code changes better
- Top 20 detection results typically show near-100% precision

## 🤝 Contributing

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/new-algorithm`
3. Write code and tests
4. Commit changes: `git commit -am 'Add new similarity algorithm'`
5. Push branch: `git push origin feature/new-algorithm`
6. Submit a Pull Request

### Code Standards

- Use type annotations
- Add detailed docstrings
- Write comprehensive unit tests
- Update README documentation

## 👥 Team Members

- Project Lead: [Your Name]
- Core Contributors: [Team Member Names]

## ❓ FAQ

**Q: How to adjust similarity weights?**

A: Set `jaccard_weight` and `lcs_weight` parameters when creating `SimilarityEngine`.

**Q: How to handle other programming languages?**

A: Modify tokenization rules in `src/core/preprocessor.py`.

**Q: How to improve detection speed?**

A: Reduce `k` value or implement parallel processing.

**Q: Test data not realistic enough?**

A: Edit templates in `test_generator.py` to add more realistic programming patterns.

## 📄 License

This project uses the MIT License.

---

If you encounter issues during usage, check the log output or submit an Issue. Happy detecting! 🎯