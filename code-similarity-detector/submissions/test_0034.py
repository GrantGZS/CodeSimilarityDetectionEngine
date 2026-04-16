def get_most_common(count):
    if not count:
        return None
    return max(count.items(), key=lambda x: x[1])


def count_words(text):
    words = text.split()
    count = {}
    for word in words:
        word = word.lower().strip('.,!?')
        if word in count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count
