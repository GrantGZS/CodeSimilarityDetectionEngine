## Create a class named SimilarityEngine that takes a parameter k in its constructor.
# Then, implement a method 'get_shingles(self, tokens)' that converts a list of strings 
# into a set of k-grams (tuples of length k).

class SimilarityEngine:
    def __init__(self, k):
        self.k = k

    def get_shingles(self, tokens):
        shingles = set()
        for i in range(len(tokens) - self.k + 1):
            shingle = tuple(tokens[i:i + self.k])
            shingles.add(shingle)
        return shingles
## Next, implement a method 'jaccard_similarity(self, shingles1, shingles2)' that calculates the Jaccard similarity between two sets of shingles.
    def jaccard_similarity(self, shingles1, shingles2):
        intersection = shingles1.intersection(shingles2)
        union = shingles1.union(shingles2)
        if not union:
            return 0.0
        return len(intersection) / len(union)
## Finally, implement a method 'similarity(self, tokens1, tokens2)' that takes two lists of strings, converts them into shingles using 'get_shingles', and returns their Jaccard similarity using 'jaccard_similarity'.
    def similarity(self, tokens1, tokens2):
        shingles1 = self.get_shingles(tokens1)
        shingles2 = self.get_shingles(tokens2)
        return self.jaccard_similarity(shingles1, shingles2)
### Implement a method 'compute_lcs(self, tokens_a, tokens_b)' 
# using dynamic programming to find the Longest Common Subsequence length.
# Normalize the result by dividing the LCS length by the maximum length of the two input lists.
    def compute_lcs(self, tokens_a, tokens_b):
        m = len(tokens_a)
        n = len(tokens_b)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if tokens_a[i - 1] == tokens_b[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

        lcs_length = dp[m][n]
        max_length = max(m, n)
        if max_length == 0:
            return 0.0
        return lcs_length / max_length