# LCS length (space-optimized two-row DP)
def lcs_length(a: list[str], b: list[str]) -> int:
    # Return the length of the Longest Common Subsequence of *a* and *b*
    # Uses the classic two-row rolling-array DP to keep memory at O(m) instead of O(mn)
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return 0

    # Ensure b is the shorter sequence (optimizes the inner loop)
    if n < m:
        a, b = b, a
        n, m = m, n

    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev, curr = curr, [0] * (m + 1)

    return prev[m]

def lcs_similarity(a: list[str], b: list[str]) -> float:
    # Normalized LCS similarity score in [0.0, 1.0]
    if not a and not b:
        return 0.0
    length = lcs_length(a, b)
    return length / max(len(a), len(b))

# Optional: Longest Matching Segment (contiguous)
def longest_matching_segment(a: list[str], b: list[str]) -> tuple[int, int, int]:
    n, m = len(a), len(b)
    if n == 0 or m == 0:
        return (0, 0, 0)

    # Keep b as the column dimension (inner loop)
    if n < m:
        a, b = b, a
        n, m = m, n
        swapped = True
    else:
        swapped = False

    best_len   = 0
    best_end_a = 0
    best_end_b = 0

    prev = [0] * (m + 1)
    curr = [0] * (m + 1)

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                curr[j] = prev[j - 1] + 1
                if curr[j] > best_len:
                    best_len   = curr[j]
                    best_end_a = i
                    best_end_b = j
            else:
                curr[j] = 0
        prev, curr = curr, [0] * (m + 1)

    start_a = best_end_a - best_len
    start_b = best_end_b - best_len

    if swapped:
        # swap back so indices refer to original a/b
        start_a, start_b = start_b, start_a

    return (best_len, start_a, start_b)


def extract_segment_tokens(tokens: list[str], start: int, length: int) -> list[str]:
    # Helper: return the matching segment as a token list
    return tokens[start : start + length]