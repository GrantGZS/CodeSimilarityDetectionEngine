"""
Similarity Detection Reporter.

This script performs pairwise similarity comparisons on test files,
generates ranked lists of suspicious file pairs and false positives,
and produces reports.
"""

import os
import json
import time
from typing import List, Dict, Any, Tuple
from pathlib import Path
from itertools import combinations

# Import core modules
from src.core import SimilarityEngine, preprocess_file
from src.utils.logger import get_logger

logger = get_logger(__name__)


def load_ground_truth(ground_truth_path: str = "ground_truth.json") -> Dict[str, List[str]]:
    """Load ground truth similarity pairs."""
    try:
        with open(ground_truth_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Ground truth file {ground_truth_path} not found")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing ground truth: {e}")
        return {}


def get_test_files(submissions_dir: str = "submissions") -> List[str]:
    """Get list of Python files in submissions directory."""
    if not os.path.exists(submissions_dir):
        raise FileNotFoundError(f"Submissions directory '{submissions_dir}' not found")
    
    files = []
    for filename in os.listdir(submissions_dir):
        if filename.endswith('.py'):
            files.append(filename)
    
    files.sort()  # Ensure consistent ordering
    logger.info(f"Found {len(files)} Python files in {submissions_dir}")
    return files


def is_true_positive(file1: str, file2: str, ground_truth: Dict[str, List[str]]) -> bool:
    """Check if a file pair is a true positive based on ground truth."""
    return file2 in ground_truth.get(file1, [])


def perform_pairwise_comparison(
    files: List[str], 
    submissions_dir: str,
    ground_truth: Dict[str, List[str]]
) -> List[Dict[str, Any]]:
    """
    Perform pairwise similarity comparison on all file pairs.
    
    Returns list of comparison results sorted by similarity (descending).
    """
    logger.info("Starting pairwise comparisons...")
    
    engine = SimilarityEngine()
    results = []
    total_pairs = len(list(combinations(files, 2)))
    processed = 0
    
    start_time = time.time()
    
    for file1, file2 in combinations(files, 2):
        try:
            # Preprocess files
            path1 = os.path.join(submissions_dir, file1)
            path2 = os.path.join(submissions_dir, file2)
            
            tokens1 = preprocess_file(path1)
            tokens2 = preprocess_file(path2)
            
            # Calculate similarity
            similarity = engine.get_final_score(tokens1, tokens2)
            
            # Check ground truth
            true_positive = is_true_positive(file1, file2, ground_truth)
            
            result = {
                "file1": file1,
                "file2": file2,
                "similarity": round(similarity, 4),
                "is_true_positive": true_positive
            }
            
            results.append(result)
            processed += 1
            
            # Progress logging
            if processed % 100 == 0:
                elapsed = time.time() - start_time
                logger.info(f"Processed {processed}/{total_pairs} pairs ({processed/total_pairs*100:.1f}%) - {elapsed:.1f}s")
            
        except Exception as e:
            logger.error(f"Error comparing {file1} vs {file2}: {e}")
            continue
    
    # Sort by similarity descending
    results.sort(key=lambda x: x["similarity"], reverse=True)
    
    elapsed_total = time.time() - start_time
    logger.info(f"Completed {len(results)} comparisons in {elapsed_total:.1f}s")
    
    return results


def generate_top_suspicious(results: List[Dict[str, Any]], top_n: int = 20) -> List[Dict[str, Any]]:
    """Extract top N suspicious file pairs (highest similarity, regardless of ground truth)."""
    return results[:top_n]


def generate_top_false_positives(results: List[Dict[str, Any]], top_n: int = 20) -> List[Dict[str, Any]]:
    """Extract top N false positive pairs (highest similarity among non-similar pairs)."""
    false_positives = [r for r in results if not r["is_true_positive"]]
    return false_positives[:top_n]


def calculate_statistics(
    results: List[Dict[str, Any]], 
    top_suspicious: List[Dict[str, Any]],
    top_false_positives: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """Calculate performance statistics."""
    total_comparisons = len(results)
    true_positives_total = sum(1 for r in results if r["is_true_positive"])
    false_positives_total = total_comparisons - true_positives_total
    
    # Top suspicious stats
    tp_in_suspicious = sum(1 for r in top_suspicious if r["is_true_positive"])
    precision_suspicious = tp_in_suspicious / len(top_suspicious) if top_suspicious else 0
    
    # Top false positives stats (should all be false positives)
    fp_in_false_pos = len(top_false_positives)  # All should be false positives
    
    # Overall recall (if we know total true positives)
    # Since each group has C(10,2)=45 true pairs, and 5 groups: 5*45=225
    total_true_pairs = 225  # 5 templates * C(10,2)
    recall_suspicious = tp_in_suspicious / total_true_pairs if total_true_pairs > 0 else 0
    
    return {
        "total_comparisons": total_comparisons,
        "true_positives_total": true_positives_total,
        "false_positives_total": false_positives_total,
        "total_true_pairs": total_true_pairs,
        
        # Top suspicious stats
        "precision_top_suspicious": round(precision_suspicious, 4),
        "recall_top_suspicious": round(recall_suspicious, 4),
        "true_positives_in_top_suspicious": tp_in_suspicious,
        
        # Top false positives stats
        "false_positives_in_top_false_pos": fp_in_false_pos,
    }


def save_results(
    results: List[Dict[str, Any]], 
    top_suspicious: List[Dict[str, Any]],
    top_false_positives: List[Dict[str, Any]],
    stats: Dict[str, Any], 
    output_file: str = "results.json"
):
    """Save results to JSON file."""
    output_data = {
        "all_comparisons": results,
        "top_20_suspicious": top_suspicious,
        "top_20_false_positives": top_false_positives,
        "statistics": stats,
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    
    logger.info(f"Results saved to {output_file}")


def print_terminal_report(
    top_suspicious: List[Dict[str, Any]], 
    top_false_positives: List[Dict[str, Any]],
    stats: Dict[str, Any]
):
    """Print a beautiful terminal report."""
    print("\n" + "="*100)
    print("🎯 CODE SIMILARITY DETECTION REPORT")
    print("="*100)
    
    print(f"\n📊 STATISTICS:")
    print(f"   Total Comparisons: {stats['total_comparisons']:,}")
    print(f"   True Positives (Total): {stats['true_positives_total']}")
    print(f"   False Positives (Total): {stats['false_positives_total']}")
    print(f"   Total True Pairs (Ground Truth): {stats['total_true_pairs']}")
    
    print(f"\n🎯 TOP 20 SUSPICIOUS PAIRS (Highest Similarity Overall):")
    print(f"   Precision: {stats['precision_top_suspicious']:.1%}")
    print(f"   Recall: {stats['recall_top_suspicious']:.1%}")
    print(f"   True Positives: {stats['true_positives_in_top_suspicious']}/20")
    print("-" * 100)
    print(f"{'Rank':<4} {'File 1':<15} {'File 2':<15} {'Similarity':<10} {'Type'}")
    print("-" * 100)
    
    for i, result in enumerate(top_suspicious, 1):
        tp_marker = "✅ TP" if result["is_true_positive"] else "❌ FP"
        print(f"{i:<4} {result['file1']:<15} {result['file2']:<15} {result['similarity']:<10.4f} {tp_marker}")
    
    print(f"\n❌ TOP 20 FALSE POSITIVES (Highest Similarity Among Non-Similar Pairs):")
    print(f"   False Positives: {stats['false_positives_in_top_false_pos']}/20")
    print("-" * 100)
    print(f"{'Rank':<4} {'File 1':<15} {'File 2':<15} {'Similarity':<10}")
    print("-" * 100)
    
    for i, result in enumerate(top_false_positives, 1):
        print(f"{i:<4} {result['file1']:<15} {result['file2']:<15} {result['similarity']:<10.4f}")
    
    print("\n" + "="*100)
    print("✅ Report generation complete!")
    print("📄 Full results saved to results.json")
    print("="*100)


def main():
    """Main execution function."""
    logger.info("Starting similarity detection reporter")
    
    try:
        # Load ground truth
        ground_truth = load_ground_truth()
        
        # Get test files
        files = get_test_files()
        
        if len(files) < 2:
            logger.error("Need at least 2 files for comparison")
            return
        
        # Perform comparisons
        results = perform_pairwise_comparison(files, "submissions", ground_truth)
        
        # Generate top lists
        top_suspicious = generate_top_suspicious(results)
        top_false_positives = generate_top_false_positives(results)
        
        # Calculate statistics
        stats = calculate_statistics(results, top_suspicious, top_false_positives)
        
        # Save results
        save_results(results, top_suspicious, top_false_positives, stats)
        
        # Print report
        print_terminal_report(top_suspicious, top_false_positives, stats)
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise


if __name__ == "__main__":
    main()