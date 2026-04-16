def count_words(text):
    words = text.split()
    word_count = {}
    for word in words:
        word = word.lower().strip('.,!?')
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


def get_most_common(word_count):
    if not word_count:
        return None
    return max(word_count.items(), key=lambda x: x[1])
