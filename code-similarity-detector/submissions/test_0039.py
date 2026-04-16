
def count_words(text):
    words = text.split()
    data = {}
    for word in words:
        word = word.lower().strip('.,!?')
        if word in data:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

def get_most_common(data):
    if not data:
        return None
    return max(data.items(), key=lambda x: x[1])
