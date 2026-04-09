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

    # Initialize SimilarityEngine with k=3
    engine = SimilarityEngine(k=3)

    # Collect results
    results = []

    for case_key, description in case_descriptions.items():
        if case_key in test_cases:
            tokens_a = test_cases[case_key]['file_a']
            tokens_b = test_cases[case_key]['file_b']

            # Compute Jaccard similarity
            jaccard_score = engine.similarity(tokens_a, tokens_b)

            # Compute LCS similarity
            lcs_score = engine.compute_lcs(tokens_a, tokens_b)

            # Compute Combined score (average of Jaccard and LCS)
            combined_score = (jaccard_score + lcs_score) / 2

            results.append({
                'description': description,
                'jaccard': jaccard_score,
                'lcs': lcs_score,
                'combined': combined_score
            })

    # Print results in table format
    print("\nCode Similarity Detection Test Results")
    print("=" * 80)
    print(f"{'Test Case':<25} {'Jaccard':<15} {'LCS':<15} {'Combined':<15}")
    print("-" * 80)

    for result in results:
        print(f"{result['description']:<25} "
              f"{result['jaccard']:.4f}          "
              f"{result['lcs']:.4f}          "
              f"{result['combined']:.4f}")

    print("=" * 80)

    # Print analysis summary
    print("\nAnalysis Summary:")
    print("-" * 80)
    for result in results:
        print(f"\n{result['description']}:")
        print(f"  Jaccard Similarity:  {result['jaccard']:.4f} (shingle-based)")
        print(f"  LCS Similarity:      {result['lcs']:.4f} (sequence-based)")
        print(f"  Combined Score:      {result['combined']:.4f} (average)")

    # Performance insights
    print("\n" + "=" * 80)
    print("Performance Insights:")
    print("-" * 80)

    identical = results[0]
    renamed = results[1]
    structural = results[2]

    print(f"\nIdentical Code Detection:")
    print(f"  Both methods should score high: Jaccard={identical['jaccard']:.4f}, LCS={identical['lcs']:.4f}")

    print(f"\nRenamed Variables Detection:")
    print(f"  Methods may differ: Jaccard={renamed['jaccard']:.4f}, LCS={renamed['lcs']:.4f}")

    print(f"\nStructural Changes Detection:")
    print(f"  Methods may differ: Jaccard={structural['jaccard']:.4f}, LCS={structural['lcs']:.4f}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()