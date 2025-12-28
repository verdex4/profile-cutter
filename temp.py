def product(*iterables, repeat=1):
    # product('ABCD', 'xy') → Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) → 000 001 010 011 100 101 110 111

    if repeat < 0:
        raise ValueError('repeat argument cannot be negative')
    # создаем len(iterables)*repeat пулов
    pools = [tuple(pool) for pool in iterables] * repeat

    result = [[]] # внутренние списки - для комбинаций, внешний для хранения всех комбинаций
    for pool in pools:
        # эквивалентно двойному циклу x -> y
        # с каждым пулом добавляем новый уровень в комбинации
        result = [x+[y] for x in result for y in pool]

    for prod in result:
        yield tuple(prod)
    

def product_iterative(*iterables, repeat=1):
    pools = [tuple(pool) for pool in iterables] * repeat
    n = len(pools)
    
    if n == 0:
        yield ()
        return
    
    # создаем список индексов
    indices = [0] * n
    lengths = [len(pool) for pool in pools]
    
    while True:
        # генерируем текущую комбинацию
        yield tuple(pools[i][indices[i]] for i in range(n))
        
        # ищем разряд для увеличения (справа налево)
        for i in reversed(range(n)):
            if indices[i] < lengths[i] - 1:
                indices[i] += 1
                # обнуляем все разряды справа
                for j in range(i+1, n):
                    indices[j] = 0
                break
        else:
            # цикл завершен без break -> все комбинации рассмотрены
            return  

#for x in product_iterative(*[range(3)], repeat=2):
    #print(x)

def test():
    d = {"a": 1, "b": 2}
    if "a" in d:
        print("founded")
    print(len(d))

test()