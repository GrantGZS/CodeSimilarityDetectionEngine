import json
from src.engine import SimilarityEngine

def main():
    # Load the mock token data
    with open('data/mock_tokens/sample_pairs.json', 'r') as f:
        test_cases = json.load(f)

    # Define test case descriptions
    case_descriptions = {
        'case_1_identical': 'Identical code',
        'case_2_renamed': 'Renamed variables',
        'case_3_structural_change': 'Structural changes'
    }

    print("Code Similarity Detection Test Results")
    print("=" * 50)

    for case_key, description in case_descriptions.items():
        if case_key in test_cases:
            tokens_a = test_cases[case_key]['file_a']
            tokens_b = test_cases[case_key]['file_b']

            # Create SimilarityEngine with k=3
            engine = SimilarityEngine(k=3)

            # Compute Jaccard similarity
            jaccard_score = engine.similarity(tokens_a, tokens_b)

            # Compute LCS similarity
            lcs_score = engine.compute_lcs(tokens_a, tokens_b)

            print(f"\n{description}:")
            print(f"  Jaccard Similarity: {jaccard_score:.3f}")
            print(f"  LCS Similarity: {lcs_score:.3f}")
        else:
            print(f"\n{description}: Test case '{case_key}' not found in data")

if __name__ == "__main__":
    main()