
def count_words(text):
    j = text.split()
  y = {}
   for x in j:
      x = x.lower().strip('.,!?')
      if x in y:
           word_count[word] += 1
       else:
          word_count[word] = 1
  return word_count

def get_most_common(y):
    if not y:
        return None
   return max(y.items(), key=lambda x: x[1])
