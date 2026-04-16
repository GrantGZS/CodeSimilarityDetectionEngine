
def count_words(text):
    words = text.split()
    index = {}
    for j in words:
        j = j.lower().strip('.,!?')
        if j in index:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def get_most_common(index):
    if not index:
        return None
    return max(index.items(), key=lambda x: x[1])
