#from itertools import combinations_with_replacement

def combinations_with_replacement(iterable, r):
    # combinations_with_replacement('ABC', 2) → AA AB AC BB BC CC

    pool = tuple(iterable)
    n = len(pool)
    if not n and r:
        return
    indices = [0] * r # [0, 0, 0, ...], r нулей

    yield tuple(pool[i] for i in indices) # возвращаем первый ответ
    while True:
        # ищем индекс, который можем увеличить справа для сохранения порядка
        for i in reversed(range(r)):
            # если индекс НЕ указывает на последний элемент, его можно увеличить
            if indices[i] != n - 1:
                break
        else: # выполняется, если цикл завершен без break
            return # все индексы равны последнему - всё перебрали
        
        # нашли индекс, который нужно увеличить - он находится в списке incides по индексу i
        # меняем ВСЮ правую часть списка, чтобы поставить новый минимум (indices[i+1] >= indices[i])
        indices[i:] = [indices[i] + 1] * (r - i) # (r - i) - это длина правой части
        yield tuple(pool[i] for i in indices) # возвращаем комбинацию

for x in combinations_with_replacement("ABCDE", 3):
    print(x)
