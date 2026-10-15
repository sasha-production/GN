def func(path: str):
    """
    Возвращает значение по пути 'a.b.c' во вложенном словаре.
    Если ключа нет — вернёт None (или можно бросить исключение).
    """
    data = {
    'a': {
        'b': {
            'c': '+++'
            }
        }
    }
    current = data
    for key in path.split('.'):
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


if __name__ == '__main__':
    line = input()
    print(func(line))