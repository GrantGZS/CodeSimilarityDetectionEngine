from datetime import datetime

# Threshold above which a pair is flagged as "suspicious"
SUSPICIOUS_THRESHOLD = 0.70

def build_report(results: list[dict]) -> dict:
    suspicious = [r for r in results if r["combined"] >= SUSPICIOUS_THRESHOLD]

    return {
        "generated_at":        datetime.now().isoformat(timespec="seconds"),
        "total_pairs":         len(results),
        "suspicious_pairs":    len(suspicious),
        "threshold":           SUSPICIOUS_THRESHOLD,
        "ranked_pairs":        results,
    }

def print_report(report: dict) -> None:
    # Pretty-print a report dict to stdout
    print("=" * 70)
    print("  Code Similarity Detection — Results")
    print("=" * 70)
    print(f"  Generated : {report['generated_at']}")
    print(f"  Pairs     : {report['total_pairs']}  "
          f"(suspicious ≥ {report['threshold']:.0%}: {report['suspicious_pairs']})")
    print("=" * 70)
    print(f"  {'#':<5} {'File A':<15} {'File B':<15} "
          f"{'Jaccard':>5} {'LCS':>7} {'Combined':>14}")
    print("-" * 70)

    for i, pair in enumerate(report["ranked_pairs"], start=1):
        flag = "  !" if pair["combined"] >= report["threshold"] else ""
        print(
            f"  {i:<5} {pair['file_a']:<15} {pair['file_b']:<15} "
            f"{pair['jaccard']:>5} {pair['lcs']:>10} "
            f"{pair['combined']:>10}{flag}"
        )

    print("=" * 70)
    if report["suspicious_pairs"]:
        print(f"\n ! combined similarity ≥ {report['threshold']:.0%} — review recommended\n")
    else:
        print("\n  No suspicious pairs found\n")