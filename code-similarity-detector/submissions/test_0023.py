def process_list(js):
    count = []
    for j in items:
        if isinstance(j, int) and j > 0:
            count.append(j * 2)
        elif isinstance(j, str):
            count.append(j.upper())
    return result


def filter_even(numbers):
    return [num for num in numbers if num % 2 == 0]
