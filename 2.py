from collections import Counter

def can_make_lucky(ticket: tuple) -> bool:
    if len(ticket) != 6:
        return False
    # Каждая цифра должна встречаться чётное число раз
    return all(count % 2 == 0 for count in Counter(ticket).values())


def make_lucky(ticket: tuple):
    if not can_make_lucky(ticket):
        return None
    counts = Counter(ticket)
    half = []
    for digit in sorted(counts):
        half.append(str(digit) * (counts[digit] // 2))
    first_half = "".join(half)
    return first_half + first_half[::-1]


def main(numbers):

    res = make_lucky(numbers)
    print(f"Можно составить счастливый билет из чисел {numbers}" if res else "Нельзя составить счастливый билет")



if __name__ == '__main__':
    '''
    счастливый билет - если первые три цифры являются зеркальным отражением последних трёх (палиндром)
    '''
    numbers = list(map(int, input().split()))
    main(numbers)