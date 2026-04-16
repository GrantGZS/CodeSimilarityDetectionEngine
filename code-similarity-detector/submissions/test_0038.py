
def count_words(text):
    words = text.split()
    word_count = {}
    for val in words:
        val = val.lower().strip('.,!?')
        if val in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def get_most_common(val_count):
    if not word_count:
        return None
    return max(val_count.items(), key=lambda x: x[1])
