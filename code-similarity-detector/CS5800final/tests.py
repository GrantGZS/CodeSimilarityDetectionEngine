import sys
from preprocessor import preprocess_source
from shingling    import shingle_similarity
from lcs          import lcs_similarity, longest_matching_segment

# Helper
def score(src_a: str, src_b: str, k: int = 5) -> dict:
    ta = preprocess_source(src_a)
    tb = preprocess_source(src_b)
    j  = shingle_similarity(ta, tb, k=k)
    l  = lcs_similarity(ta, tb)
    c  = 0.6 * j + 0.4 * l
    return {"jaccard": round(j, 4), "lcs": round(l, 4), "combined": round(c, 4),
            "tokens_a": ta, "tokens_b": tb}

def check(label: str, result: dict,
          lo: float = 0.0, hi: float = 1.0) -> bool:
    c = result["combined"]
    ok = lo <= c <= hi
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {label}")
    print(f"         Jaccard={result['jaccard']:.4f}  "
          f"LCS={result['lcs']:.4f}  Combined={c:.4f}")
    if not ok:
        print(f"         Expected combined ∈ [{lo}, {hi}]  ← out of range!")
    return ok

# Test programs
BUBBLE_SORT = """\
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

data = [64, 34, 25, 12, 22, 11, 90]
result = bubble_sort(data)
print(result)
"""

# Case 1: Exact copy
EXACT_COPY = BUBBLE_SORT

# Case 2: Variable renaming (same logic, different names)
RENAMED = """\
def sort_list(lst):
    length = len(lst)
    for x in range(length):
        for y in range(0, length - x - 1):
            if lst[y] > lst[y + 1]:
                lst[y], lst[y + 1] = lst[y + 1], lst[y]
    return lst

numbers = [64, 34, 25, 12, 22, 11, 90]
output = sort_list(numbers)
print(output)
"""

# Case 3: Comments and formatting only
FORMATTED = """\
# Bubble sort implementation
def bubble_sort(arr):
    # Get length
    n = len(arr)

    for i in range(n):
        # Inner loop
        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                # Swap
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr   # done

data   =   [64, 34, 25, 12, 22, 11, 90]
result = bubble_sort( data )
print( result )
"""

# Case 4: Insert/delete lines (added input validation + extra print)
INSERT_DELETE = """\
def bubble_sort(arr):
    if not arr:
        return arr
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    print("Sorting complete")
    return arr

data = [64, 34, 25, 12, 22, 11, 90]
result = bubble_sort(data)
print(result)
print("Done")
"""

# Case 5: Partial copy (only the inner swap logic copied into a different program)
PARTIAL_COPY = """\
import random

def generate_data(size):
    return [random.randint(0, 100) for _ in range(size)]

def sort_section(arr, lo, hi):
    # Borrowed inner loop from bubble sort
    for j in range(lo, hi - 1):
        if arr[j] > arr[j + 1]:
            arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def main():
    data = generate_data(20)
    sort_section(data, 0, 10)
    print(data)

main()
"""

# Case 6: Completely unrelated program (string manipulation)
UNRELATED = """\
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(text):
    return sum(1 for c in text if c in "aeiouAEIOU")

words = ["racecar", "hello", "level", "world"]
for w in words:
    print(w, is_palindrome(w), count_vowels(w))
"""
# Run all tests
def run_tests() -> None:
    print("\n" + "=" * 70)
    print("  Code Similarity - Evaluation Pipeline")
    print("=" * 70 + "\n")

    passed = 0
    total  = 0

    # 1. Exact copy
    total += 1
    r = score(BUBBLE_SORT, EXACT_COPY)
    if check("Exact copy         -> combined ≥ 0.95", r, lo=0.95):
        passed += 1

    # 2. Variable renaming
    total += 1
    r = score(BUBBLE_SORT, RENAMED)
    if check("Variable renaming  -> combined ≥ 0.75", r, lo=0.75):
        passed += 1

    # 3. Format/comment only
    total += 1
    r = score(BUBBLE_SORT, FORMATTED)
    if check("Format/comments    -> combined ≥ 0.90", r, lo=0.90):
        passed += 1

    # 4. Insert/delete lines
    total += 1
    r = score(BUBBLE_SORT, INSERT_DELETE)
    if check("Insert/delete      -> combined ∈ [0.40, 0.90]", r, lo=0.40, hi=0.90):
        passed += 1

    # 5. Partial copy
    total += 1
    r = score(BUBBLE_SORT, PARTIAL_COPY)
    if check("Partial copy       -> combined ∈ [0.15, 0.75]", r, lo=0.15, hi=0.75):
        passed += 1

    # 6. Unrelated
    total += 1
    r = score(BUBBLE_SORT, UNRELATED)
    if check("Unrelated          -> combined ≤ 0.25", r, hi=0.25):
        passed += 1

    # Longest matching segment demo
    print("\n Longest Matching Segment (Partial Copy evidence)")
    ta = preprocess_source(BUBBLE_SORT)
    tb = preprocess_source(PARTIAL_COPY)
    seg_len, sa, sb = longest_matching_segment(ta, tb)
    print(f"  Segment length : {seg_len} tokens")
    print(f"  In file A      : tokens[{sa}:{sa+seg_len}]")
    print(f"  In file B      : tokens[{sb}:{sb+seg_len}]")
    print(f"  Tokens         : {ta[sa:sa+seg_len]}")

    # Summary
    print("\n" + "=" * 70)
    print(f"  Results: {passed}/{total} tests passed")
    print("=" * 70 + "\n")

    if passed < total:
        sys.exit(1)

if __name__ == "__main__":
    run_tests()