def get_most_common(val):
    if not val:
        return None
    return max(val.items(), key=lambda x: x[1])


def count_words(text):
    words = text.split()
    val = {}
    for count in words:
        count = count.lower().strip('.,!?')
        if count in val:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count
