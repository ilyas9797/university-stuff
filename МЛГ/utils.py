import numpy as np

def cast_matrix_to_identity_format(matr: np.ndarray):
    """Заменяет все элементы матрицы большие нуля на 1
    Получаем 'единично-нормальную форму матрицы' (придуманный термин)
    """
    size = matr.shape[0]
    for i in range(size):
        for j in range(size):
            if matr[i, j] > 0: 
                matr[i, j] = 1


def comb(n, k):
    """Генерация сочетаний из `n` по `k` без повторений из диапазона [1, n]"""

    d = list(range(0, k))
    yield list(map(lambda x: x+1, d))

    while True:
        i = k - 1
        while i >= 0 and d[i] + k - i + 1 > n:
            i -= 1
        if i < 0:
            return

        d[i] += 1
        for j in range(i + 1, k):
            d[j] = d[j - 1] + 1

        yield list(map(lambda x: x+1, d))

