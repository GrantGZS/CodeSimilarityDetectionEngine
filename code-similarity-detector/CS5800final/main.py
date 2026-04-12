import argparse
import json
import sys
from pathlib import Path
from itertools import combinations

from preprocessor import preprocess_file
from shingling import shingle_similarity
from lcs import lcs_similarity
from reporter import build_report, print_report

def compare_all(py_files: list[Path], k: int) -> list[dict]:
    # Step 1 – preprocess
    token_seqs: dict[str, list[str]] = {}
    for f in py_files:
        try:
            token_seqs[f.name] = preprocess_file(f)
        except Exception as exc:
            print(f"[WARN] Could not process {f.name}: {exc}", file=sys.stderr)

    names = list(token_seqs.keys())
    results = []

    # Step 2 – pairwise comparison
    for a, b in combinations(names, 2):
        seq_a = token_seqs[a]
        seq_b = token_seqs[b]

        shin = shingle_similarity(seq_a, seq_b, k=k)
        lcs  = lcs_similarity(seq_a, seq_b)
        combined = 0.6 * shin + 0.4 * lcs

        results.append({
            "file_a":   a,
            "file_b":   b,
            "jaccard":  round(shin, 4),
            "lcs":      round(lcs,  4),
            "combined": round(combined, 4),
        })

    # Rank by combined score descending
    results.sort(key=lambda r: r["combined"], reverse=True)
    return results

def main() -> None:
    parser = argparse.ArgumentParser(description="Code Similarity Detector")
    parser.add_argument("directory", help="Folder containing .py files to compare")
    parser.add_argument("--k",   type=int, default=5,            help="Shingle (k-gram) size (default: 5)")
    parser.add_argument("--out", type=str, default="results.json", help="Output JSON file path")
    args = parser.parse_args()

    target_dir = Path(args.directory)
    if not target_dir.is_dir():
        sys.exit(f"Error: '{args.directory}' is not a directory.")

    py_files = sorted(target_dir.glob("*.py"))
    if len(py_files) < 2:
        sys.exit("Need at least 2 .py files to compare.")

    print(f"Found {len(py_files)} Python files. Running pairwise comparison (k={args.k})...\n")

    results = compare_all(py_files, k=args.k)
    report  = build_report(results)

    # Write JSON
    out_path = Path(args.out)
    out_path.write_text(json.dumps(report, indent=2))
    print(f"Results written to {out_path}\n")

    # Pretty-print to stdout
    print_report(report)

if __name__ == "__main__":
    main()