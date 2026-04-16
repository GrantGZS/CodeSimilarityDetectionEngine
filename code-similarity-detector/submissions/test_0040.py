def count_words(text):
    words = text.split()
    i = {}
    for z in words:
        z = z.lower().strip('.,!?')
        if z in i:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count


def get_most_common(i):
    if not i:
        return None
    return max(i.items(), key=lambda x: x[1])
