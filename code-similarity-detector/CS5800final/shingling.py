def build_shingles(tokens: list[str], k: int = 5) -> set[tuple[str, ...]]:
    # Each element is a k-length tuple of token strings
    # Returns an empty set if len(tokens) < k
    if len(tokens) < k:
        return set()
    return {tuple(tokens[i : i + k]) for i in range(len(tokens) - k + 1)}


def jaccard(set_a: set, set_b: set) -> float:
    # Compute the Jaccard similarity coefficient between two sets
    # Returns 0.0 when both sets are empty (avoids division by zero)
    if not set_a and not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union        = len(set_a | set_b)
    return intersection / union

def shingle_similarity(tokens_a: list[str], tokens_b: list[str], k: int = 5) -> float:
    # Returns Jaccard similarity in [0.0, 1.0]
    # 1.0 -> identical shingle sets, 0.0 -> completely disjoint
    shingles_a = build_shingles(tokens_a, k)
    shingles_b = build_shingles(tokens_b, k)
    return jaccard(shingles_a, shingles_b)