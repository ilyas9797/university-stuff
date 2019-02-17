import numpy as np
from typing import List, Tuple
import os
from inspect import stack



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


def write_matrix(file_name: str, matr: np.ndarray) -> None:
    """Запись матрицы matr в файл write_matrix"""
    np.set_printoptions(threshold=np.nan, linewidth=np.nan)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name,'w') as file:
        file.write(str(matr))

def write_exponents(file_name: str, results: List[Tuple[int, List[int], int]]) -> None:
    """Запись информации об изученных МЛГ, перечисленной в results, в файл file_name

    results - список с информацией об изученных МЛГ, элементы которого имеют вид (ppnum, pp, power), где    
        ppnum - количество точек съема
        
        pp - список номеров точек съема
        
        power - экспонент данного МЛГ
    """
    np.set_printoptions(threshold=np.nan, linewidth=np.nan)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as file:
        file.write("<Pickup points> --- <Exponent>\n")
        file.write('\n'.join(f"{r[1]} --- {r[2]}" for r in results))

def write_perf_index(file_name: str, results: List[Tuple[int, List[int], int]]) -> None:
    """
    results - список с информацией об изученных МЛГ, элементы которого имеют вид (ppnum, pp, perf_index), где    
        ppnum - количество точек съема
        
        pp - список номеров точек съема
        
        perf_index - 
    """
    np.set_printoptions(threshold=np.nan, linewidth=np.nan)
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w') as file:
        file.write("<Pickup points> --- <Index of perfection>\n")
        file.write('\n'.join(f"{r[1]} --- {r[2]}" for r in results))

def progress_info(message: str) -> None:
    print(f"{stack()[1][3]}: {message}")



