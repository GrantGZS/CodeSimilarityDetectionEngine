
def process_list(items):
   result = []
  for item in items:
      if isinstance(item, int) and item > 0:
           result.append(item * 2)
        elif isinstance(item, str):
           result.append(item.upper())
   return result

def filter_even(numbers):
  return [num for num in numbers if num % 2 == 0]
